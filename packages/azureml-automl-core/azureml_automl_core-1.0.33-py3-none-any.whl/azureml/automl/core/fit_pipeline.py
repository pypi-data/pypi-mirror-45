# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Code used to fit pipeline."""
from typing import Any, Dict, Optional
import json
import logging

import numpy as np
import scipy
import sklearn.pipeline

from automl.client.core.common import constants, logging_utilities, utilities, memory_utilities
from . import data_transformation, pipeline_run_helper, training_utilities
from .automl_base_settings import AutoMLBaseSettings
from .automl_pipeline import AutoMLPipeline
from .automl_run_context import AutoMLAbstractRunContext
from .cache_store import FileCacheStore
from .fit_output import FitOutput
from .data_context import RawDataContext, TransformedDataContext
from .ensemble_base import EnsembleBase
from .systemusage_telemetry import SystemResourceUsageTelemetryFactory
from .onnx_convert import OnnxConvertConstants, OnnxConverter


def fit_pipeline(automl_pipeline: AutoMLPipeline,
                 automl_settings: AutoMLBaseSettings,
                 automl_run_context: AutoMLAbstractRunContext,
                 fit_iteration_parameters_dict: Optional[Dict[str, Any]] = None,
                 remote: bool = True,
                 logger: logging.Logger = logging_utilities.get_logger(),
                 transformed_data_context: Optional[TransformedDataContext] = None,
                 elapsed_time: Optional[int] = None,
                 onnx_cvt: Optional[OnnxConverter] = None) -> FitOutput:
    """
    Run a single iteration of an AutoML experiment.

    This method is automatically called during a regular AutoML
    experiment. fit_pipeline will evaluate the pipeline for this iteration, fit the pipeline with the provided data,
    calculate the various metrics relevant for this experiment, and log all the results in the specified AzureML Run's
    history.

    :param automl_pipeline: AutoMLPipeline object containing pipeline id and serialized script.
    :param automl_settings: User settings specified when creating AutoMLConfig.
    :param automl_run_context: child run context object
    :param fit_iteration_parameters_dict: Remaining data specific parameters for fit such as 'x_raw_column_names'.
    :param remote: flag whether this is a remote run or local run.
    :param logger: logger for info/error messages.
    :param transformed_data_context: Containing X, y and other transformed data info.
    :param elapsed_time: How long this experiment has already taken in minutes
    :param onnx_cvt: The onnx converter.
    :return: AzureML Run Properties for this child run
    """
    logging_utilities.log_system_info(logger, prefix_message="[RunId:{}]".format(automl_run_context.run_id))

    telemetry_logger = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(
        logger, interval=10)

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Starting fit_pipeline]".format(automl_run_context.run_id),
        is_sending_telemetry=automl_settings.send_telemetry
    )

    X, y, X_valid, y_valid, sample_weight, sample_weight_valid, cv_splits_indices, x_raw_column_names = _extract_data(
        fit_iteration_parameters_dict, transformed_data_context
    )

    # validate X and y
    training_utilities.validate_training_data(X, y, X_valid, y_valid, sample_weight, sample_weight_valid,
                                              cv_splits_indices, automl_settings)

    # logging X and y info
    logger.info(
        "[ParentRunId:{}] X datatype is {}, shape is {}, datasize is {}.".format(
            automl_run_context.run_id, type(X), X.shape, memory_utilities.get_data_memory_size(X)
        )
    )
    logger.info(
        "[ParentRunId:{}] y datatype is {}, shape is {}, datasize is {}.".format(
            automl_run_context.run_id, type(y), y.shape, memory_utilities.get_data_memory_size(y)
        )
    )
    if X_valid is not None:
        logger.info(
            "[ParentRunId:{}] X_valid datatype is {}, shape is {}, datasize is {}.".format(
                automl_run_context.run_id, type(X_valid), X_valid.shape, memory_utilities.get_data_memory_size(X_valid)
            )
        )
    if y_valid is not None:
        logger.info(
            "[ParentRunId:{}] y_valid datatype is {}, shape is {}, datasize is {}.".format(
                automl_run_context.run_id, type(y_valid), y_valid.shape, memory_utilities.get_data_memory_size(y_valid)
            )
        )

    logger.info("Using child run {0}".format(automl_run_context.run_id))
    fit_output = FitOutput(automl_settings, automl_pipeline)

    try:
        class_labels = None

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][Before preprocess]".format(automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        if transformed_data_context is None:
            # ignore preprocess if x is sparse
            should_preprocess = automl_settings.preprocess and not scipy.sparse.issparse(X)
            raw_data_context = RawDataContext(task_type=automl_settings.task_type,
                                              X=X,
                                              y=y,
                                              X_valid=X_valid,
                                              y_valid=y_valid,
                                              sample_weight=sample_weight,
                                              sample_weight_valid=sample_weight_valid,
                                              x_raw_column_names=x_raw_column_names,
                                              preprocess=should_preprocess,
                                              lag_length=automl_settings.lag_length,
                                              cv_splits_indices=cv_splits_indices,
                                              automl_settings_obj=automl_settings)
            cache_store = None
            if automl_settings.enable_cache:
                cache_store = FileCacheStore()
            transformed_data_context = data_transformation.transform_data(
                raw_data_context=raw_data_context, logger=logger, cache_store=cache_store,
                is_onnx_compatible=automl_settings.enable_onnx_compatible_models)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][After preprocess]".format(automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
            class_labels = np.unique(transformed_data_context.y)
            y_transformer = transformed_data_context.transformers.get('y_transformer')
            if y_transformer is not None:
                class_labels = y_transformer.inverse_transform(class_labels)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][Before executing pipeline]".format(automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        logger.info("Start executing pipeline {0}.".format(automl_pipeline.pipeline_script))
        logger.info("Running with the following AutoML settings:\n{}".format(
            automl_settings._format_selective(logging_utilities.BLACKLISTED_LOGGING_KEYS)))

        try:
            iteration_timeout_min = _check_iteration_time(automl_settings, elapsed_time)
            pipeline_run_output = pipeline_run_helper.run_pipeline(automl_settings, automl_pipeline,
                                                                   automl_run_context, iteration_timeout_min,
                                                                   transformed_data_context, logger, remote)
            fit_output.record_pipeline_results(pipeline_run_output)
        except Exception as e:
            fit_output.add_error('fit', e)
            logging_utilities.log_traceback(e, logger)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][After executing pipeline]".format(
                automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        logger.info("Pipeline execution finished with a score of {0}".format(fit_output.score))
        logger.info("Start logging metrics for child run.")
        with logging_utilities.log_activity(logger,
                                            activity_name=constants.TelemetryConstants.METRIC_AND_SAVE_MODEL_NAME,
                                            custom_dimensions={'run_id': automl_run_context.run_id}):
            with automl_run_context.get_run() as run:
                _log_metrics(run, fit_output.scores, logger)
                _log_metrics_info(fit_output.scores, logger, pipeline_id=fit_output.pipeline_id)

                automl_run_context.save_model_output(fit_output.fitted_pipeline, constants.MODEL_PATH)

                if onnx_cvt is not None:
                    # Convert to ONNX, after we got this valid fitted_pipeline.
                    # Ingect the exp name, run id data into the onnx model.
                    onnx_mdl_name = 'AutoML_ONNX_Model_[{}]'.format(run.id)
                    onnx_mdl_desc = {
                        'AutoMLSDKVer': onnx_cvt.producer_version,
                        'ExperimentName': run.experiment.name,
                        'RunId': run.id,
                        'PipeId': automl_pipeline.pipeline_id
                    }
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][Start ONNX Convert in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                    with logging_utilities.log_activity(logger,
                                                        activity_name=constants.TelemetryConstants.ONNX_CONVERSION,
                                                        custom_dimensions={'run_id': automl_run_context.run_id}):
                        onnx_model, _ = onnx_cvt.convert(raw_model=fit_output.fitted_pipeline,
                                                         model_name=onnx_mdl_name,
                                                         model_desc=onnx_mdl_desc
                                                         )
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][End ONNX Convert in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                    # If user indicates using ONNX compatible models, save the ONNX model.
                    if automl_settings.enable_onnx_compatible_models and onnx_model is not None:
                        automl_run_context.save_onnx_model_output(onnx_model, constants.MODEL_PATH_ONNX)
                need_CV_trained_models = automl_settings.enable_ensembling or \
                    (hasattr(automl_settings, "enable_stack_ensembling") and
                     automl_settings.enable_stack_ensembling)
                if need_CV_trained_models and \
                        fit_output.fitted_pipelines_train != constants.Defaults.INVALID_PIPELINE_OBJECT:
                    # we need to persist the partially trained fitted models as well
                    # they will be used for computing the scores during ensemble hill climbing
                    automl_run_context.save_model_output(fit_output.fitted_pipelines_train, constants.MODEL_PATH_TRAIN)

                # check to see if model_explainability set or not
                if automl_settings.model_explainability:
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][Start model explain in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                    try:
                        _explain_model_in_fit(run, fit_output.fitted_pipeline, transformed_data_context,
                                              class_labels, logger)
                    except Exception as e:
                        fit_output.add_error('model_explanation', e)
                        logger.warning(
                            "[RunId:{}]Failed model explanation in fit pipeline. Error Message: {}.".format(run.id, e)
                        )
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][End model explain in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )

                run.complete()
    except Exception as e:
        fit_output.add_error('overall', e)
        with automl_run_context.get_run() as run:
            logging_utilities.log_traceback(e, logger)
            run.fail()
    finally:
        # TODO: remove once backend can handle nulls
        fit_output_sanitized = fit_output.get_sanitized_output_dict()

        with automl_run_context.get_run() as run:
            run.set_tags(fit_output_sanitized)
            # TODO: move to tags once JOS is updated
            run.add_properties(fit_output_sanitized)
            run.add_properties({
                'dependencies_versions': json.dumps(utilities.get_sdk_dependencies())
            })

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][End fit_pipeline]".format(automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )
        telemetry_logger.stop()
        return fit_output


def _extract_data(fit_iteration_parameters_dict=None, transformed_data_context=None):
    # if transformed_data_context is not None, then use data in transformed_data_context. If None, then to
    # use data in fit_iteration_parameters_dict.
    if transformed_data_context is not None:
        X = transformed_data_context.X
        y = transformed_data_context.y
        X_valid = transformed_data_context.X_valid
        y_valid = transformed_data_context.y_valid
        sample_weight = transformed_data_context.sample_weight
        sample_weight_valid = transformed_data_context.sample_weight_valid
        cv_splits_indices = transformed_data_context.cv_splits_indices
        x_raw_column_names = transformed_data_context.x_raw_column_names
    elif fit_iteration_parameters_dict is not None:
        X = fit_iteration_parameters_dict.get('X')
        y = fit_iteration_parameters_dict.get('y')
        X_valid = fit_iteration_parameters_dict.get('X_valid')
        y_valid = fit_iteration_parameters_dict.get('y_valid')
        sample_weight = fit_iteration_parameters_dict.get('sample_weight')
        sample_weight_valid = fit_iteration_parameters_dict.get('sample_weight_valid')
        cv_splits_indices = fit_iteration_parameters_dict.get('cv_splits_indices')
        x_raw_column_names = fit_iteration_parameters_dict.get('x_raw_column_names')
    else:
        raise ValueError('Either a transformed data context or parameters dict is required.')
    return X, y, X_valid, y_valid, sample_weight, sample_weight_valid, cv_splits_indices, x_raw_column_names


def _check_iteration_time(automl_settings, elapsed_time):
    iteration_timeout_min = automl_settings.iteration_timeout_minutes
    if iteration_timeout_min is not None:
        iteration_timeout_min = int(iteration_timeout_min)
    if automl_settings.experiment_timeout_minutes is not None and elapsed_time is not None:
        experiment_max_time_min = int(automl_settings.experiment_timeout_minutes) - elapsed_time
        if iteration_timeout_min is None or experiment_max_time_min < iteration_timeout_min:
            iteration_timeout_min = experiment_max_time_min

    if iteration_timeout_min and iteration_timeout_min <= 0:
        raise TimeoutError('Timeout reached, skipping iteration.')

    return iteration_timeout_min


def _log_metrics_info(scores, logger, pipeline_id=None):
    reduced_scores = _get_reduced_scores(scores)
    log_fmt = "The following metrics have been logged for the child run: {}."
    if pipeline_id is not None:
        log_msg = ("pipeline_id:{}, " + log_fmt).format(pipeline_id, reduced_scores)
    else:
        log_msg = log_fmt.format(reduced_scores)
    logger.info(log_msg)


def _get_reduced_scores(scores):
    reduced_scores = dict()
    for name, score in scores.items():
        if name in constants.Metric.SCALAR_FULL_SET or score is None:
            reduced_scores[name] = score
        else:
            reduced_scores[name] = type(score)
    return reduced_scores


def _log_metrics(child_run, scores, logger):
    for name, score in scores.items():
        try:
            if name in constants.Metric.SCALAR_FULL_SET:
                child_run.log(name, score)
            elif name == constants.Metric.AccuracyTable:
                child_run.log_accuracy_table(name, score)
            elif name == constants.Metric.ConfusionMatrix:
                child_run.log_confusion_matrix(name, score)
            elif name == constants.Metric.Residuals:
                child_run.log_residuals(name, score)
            elif name == constants.Metric.PredictedTrue:
                child_run.log_predictions(name, score)
            else:
                logger.warning(
                    "Did not recognize metric: {}. Will not log.".format(name))
        except Exception as e:
            logger.warning(
                "Failed to log the metric {} with value {}, exception {}".format(name, score, e))


def _explain_model_in_fit(child_run, pipeline, transformed_data_context, class_labels, logger):
    """
    Explain the model in the fit stage and store the explanation in child_run.

    :param child_run: the run to store information
    :type child_run: azureml.core.run.Run
    :param pipeline: the pipeline to explain
    :type pipeline: sklearn.pipeline.Pipeline
    :param transformed_data_context: Containing X, y and other transformed data info
    :type transformed_data_context: TransformedDataContext
    :param class_labels: a list of unique class labels
    :param class_labels: list
    :param logger: logger for info/error messages.
    :return: None
    """
    from azureml.explain.model.mimic.mimic_explainer import MimicExplainer
    from azureml.explain.model.mimic.models.lightgbm_model import LGBMExplainableModel
    from azureml.explain.model._internal.explanation_client import ExplanationClient

    logger.info("[RunId:{}]Start model explanation in fit pipeline.".format(child_run.id))
    # Set the engineered/raw features information for model explanation
    columns = transformed_data_context._get_engineered_feature_names()

    # Convert columns from type ndarray to list
    if columns is not None and isinstance(columns, np.ndarray):
        columns = columns.tolist()

    # To explain the pipeline which should exclude datatransformer and laggingtransformer
    pipeline = EnsembleBase._transform_single_fitted_pipeline(pipeline)

    # Create the mimicexplainer
    explainer = MimicExplainer(
        pipeline, transformed_data_context.X, LGBMExplainableModel, features=columns, classes=class_labels
    )

    # Explain the model and save the explanation information to artifact
    # And don't display explain status bar
    explanation = explainer.explain_global(transformed_data_context.X_valid)
    client = ExplanationClient.from_run(child_run)
    client.upload_model_explanation(explanation, top_k=100)

    child_run.tag(constants.MODEL_EXPLANATION_TAG, 'True')

    logger.info("[RunId:{}]End model explanation in fit pipeline.".format(child_run.id))
