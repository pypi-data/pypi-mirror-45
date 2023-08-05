# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Run extensions."""

from azureml.core import Run
from ._logging._telemetry_logger import _TelemetryLogger
from ._logging._telemetry_logger_context_filter import _TelemetryLoggerContextFilter
from ._model_extensions import register_model_with_dataset

module_logger = _TelemetryLogger.get_telemetry_logger(__name__)


def register_model_and_dataset(self,
                               model_name,
                               dataset,
                               model_path=None,
                               tags=None,
                               properties=None,
                               **kwargs):
    """Register a model and a dataset for operationalization.

    :param model_name:
    :type model_name: str
    :param dataset:
    :type dataset: azureml.core.Dataset
    :param model_path: relative cloud path to model from outputs/ dir. When model_path is None, model_name is path.
    :type model_path: str
    :param tags: Dictionary of key value tags to give the model
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give the model. These properties cannot
        be changed after model creation, however new key value pairs can be added
    :type properties: dict[str, str]
    :param kwargs:
    :return:
    :rtype: azureml.core.model.Model
    """
    log_context = {'experiment_name': self.experiment.name, 'model_name': model_name}
    module_logger.addFilter(_TelemetryLoggerContextFilter(log_context))

    try:
        model = self._client.register_model(model_name, model_path, tags, properties, **kwargs)
    except Exception:
        module_logger.warning("register_model() failed: model_name: {}, model_path: {}".format(model_name,
                                                                                               model_path))
        raise

    register_model_with_dataset(model, dataset)

    return model


Run.register_model_and_dataset = register_model_and_dataset
