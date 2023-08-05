# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Model extensions."""

import random
import string

from azureml.core import Dataset
from azureml.data.dataset_snapshot import DatasetSnapshot
from azureml.core.model import Model
from azureml.exceptions import AzureMLException

from ._logging._telemetry_logger import _TelemetryLogger
from ._logging._telemetry_logger_context_filter import _TelemetryLoggerContextFilter
from .dataset_purpose import DatasetPurpose

module_logger = _TelemetryLogger.get_telemetry_logger(__name__)

# TODO, remove NAME_KEY and its references once DatasetSnapshot.get() supports Id
DATASET_ID_KEY = "_dataset_id"
DATASET_NAME_KEY = "_dataset_name"
DATASET_VERSION_KEY = "_dataset_definition_version"
DATASET_SNAPSHOT_NAME_KEY = "_dataset_snapshot_name"


def register_with_dataset(workspace, model_path, model_name, dataset, tags=None, properties=None,
                          description=None):
    """Register a model with the provided workspace.

    :param workspace: The workspace to register the model under
    :type workspace: workspace: azureml.core.workspace.Workspace
    :param model_path: Local path to model file or folder
    :type model_path: str
    :param model_name: The name to register the model with
    :type model_name: str
    :param tags: Dictionary of key value tags to give the model
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give the model. These properties cannot
        be changed after model creation, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A text description of the model
    :type description: str
    :param dataset: Dataset object to register with the model
    :type dataset: azureml.core.Dataset
    :return: The registered model object
    :rtype: Model
    """
    log_context = {'workspace_name': workspace.name, 'model_name': model_name,
                   'subscription_id': workspace.subscription_id}
    module_logger.addFilter(_TelemetryLoggerContextFilter(log_context))

    try:
        model = Model.register(workspace, model_path, model_name, tags, properties, description)
    except Exception:
        module_logger.warning(
            "Model.register() failed: workspace: {}, model_name: {}, model_path: {}".format(workspace.name,
                                                                                            model_name,
                                                                                            model_path))
        raise

    Model.register_model_with_dataset(model, dataset)

    return model


def register_model_with_dataset(model, dataset):
    """Register a given dataset with a model.

    :param model: Model object to register the dataset to
    :type model: azureml.core.model.Model
    :param dataset: Dataset object to register with the model
    :type dataset: azureml.core.Dataset
    :raises AzureMLException: Raised when the dataset is not an instance of auzrmel.core.Dataset
    :raises AzureMLException: Raised when no compute target is given
    """
    if DATASET_ID_KEY in model.properties:
        error_message = "Model {} is already registered with a dataset".format(model.id)
        module_logger.warning(error_message)
        raise AzureMLException(error_message)
    if not isinstance(dataset, Dataset):
        raise AzureMLException("dataset must be an instance of azureml.core.Dataset")

    randomized_name = Model._generate_dataset_compatible_name(model.id)

    if not (dataset.name and Dataset.get(model.workspace, name=dataset.name)):
        try:
            dataset_name = dataset.name if dataset.name else "{}_{}".format(randomized_name, "ds")
            module_logger.info("Registering dataset {} with model {}".format(dataset_name, model.id))
            dataset = dataset.register(workspace=model.workspace,
                                       name=dataset_name,
                                       description="Created within Model.register()",
                                       exist_ok=False)
        except Exception:
            module_logger.warning(
                "dataset.register() failed: workspace: {}, name: {}".format(model.workspace.name,
                                                                            dataset_name))
            raise

    try:
        snapshot_name = "{}_{}".format(randomized_name, "ss")
        compute_target = None
        if model.workspace.compute_targets:
            compute_target = next(iter(model.workspace.compute_targets.values()))
        # @TODO, remove this once non-local run is supported by dataset team
        compute_target = None
        snapshot = dataset.create_snapshot(snapshot_name=snapshot_name,
                                           compute_target=compute_target,
                                           create_data_snapshot=True)
    except Exception:
        compute_name = compute_target.name if compute_target else "<empty>"
        module_logger.warning(
            "dataset.create_snapshot() failed: snapshot: {}, compute: {}".format(snapshot_name,
                                                                                 compute_name))
        raise

    try:
        properties = dict()
        properties[DATASET_ID_KEY] = dataset.id
        properties[DATASET_NAME_KEY] = dataset.name
        properties[DATASET_VERSION_KEY] = dataset.definition_version
        properties[DATASET_SNAPSHOT_NAME_KEY] = snapshot._name
        model.add_properties(properties)
    except Exception:
        module_logger.warning("model.add_properties() failed: {}".format(properties))
        raise


@property
def datasets(self):
    """List all datasets attached to the model.

    :param dataset_purpose: Dataset purpose/relation
    :type dataset_purpose: azureml.contrib.datadrift.dataset_purpose.DatasetPurpose
    :return: Dict with key as DatasetPurpose and value as a Dataset object.
    :rtype: dict(azureml.contrib.datadrift.DatasetPurpose:azureml.core.Dataset)
    """
    result = {}
    dataset_id = None
    try:
        dataset_id = self.properties[DATASET_ID_KEY]
        result[DatasetPurpose.TRAINING] = Dataset.get(self.workspace, id=dataset_id)
    except KeyError:
        module_logger.warning("Dataset with Id {} does not exist".format(dataset_id))

    # @TODO, add model serving dataset when it is ready
    return result


def get_training_dataset_snapshot(self):
    """Get training dataset snapshot registered to the model.

    :return: Training dataset snapshot
    :rtype: azureml.core.dataset.DatasetSnapshot
    """
    dataset_snapshot_name = None
    try:
        dataset_name = self.properties[DATASET_NAME_KEY]
        dataset_snapshot_name = self.properties[DATASET_SNAPSHOT_NAME_KEY]
    except KeyError:
        module_logger.warning("Snapshot with name {} does not exist".format(dataset_snapshot_name))
        return None
    return DatasetSnapshot.get(self.workspace, dataset_snapshot_name, dataset_name)


def _compare_to(self, model):
    """Compare a DataDriftModel to a Model.

    :param model: Model object to compare to
    :type model: azureml.core.model.Model
    :raises AzureMLException: Raised when given object is not of type Model
    :return: True if objects are equal
    :rtype: bool
    """
    if not isinstance(model, Model):
        raise AzureMLException("model must be a azureml.core.model.Model type")

    return (self.created_time == model.created_time) \
        and (self.description == model.description) \
        and (self.id == model.id) \
        and (self.mime_type == model.mime_type) \
        and (self.name == model.name) \
        and (self.tags == model.tags) \
        and (self.properties == model.properties) \
        and (self.unpack == model.unpack) \
        and (self.url == model.url) \
        and (self.version == model.version) \
        and (self.workspace == model.workspace) \
        and (self._auth == model._auth) \
        and (self._mms_endpoint == model._mms_endpoint)


def _generate_dataset_compatible_name(name):
    return "{}{}".format(
        name[:15],
        "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    )


Model.datasets = datasets
Model.get_training_dataset_snapshot = get_training_dataset_snapshot
Model.register_with_dataset = register_with_dataset
Model.register_model_with_dataset = register_model_with_dataset
Model._compare_to = _compare_to
Model._generate_dataset_compatible_name = _generate_dataset_compatible_name
