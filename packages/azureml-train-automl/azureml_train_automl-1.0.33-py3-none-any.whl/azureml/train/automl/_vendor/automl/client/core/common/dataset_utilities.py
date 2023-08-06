# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utility methods for interacting with azureml.core.Dataset."""

import logging

from automl.client.core.common import logging_utilities

from .exceptions import DataprepException


_azureml_core_installed = True
_deprecated = 'deprecated'
_archived = 'archived'
module_logger = logging.getLogger(__name__)


try:
    from azureml.core import Dataset, Run
    from azureml.data.dataset_definition import DatasetDefinition
except ImportError:
    _azureml_core_installed = False


if not _azureml_core_installed:
    module_logger.debug('AzureML Core is not installed. Dataset functionalities will not work.')


def is_dataset(dataset):
    return _azureml_core_installed and isinstance(dataset, Dataset) or isinstance(dataset, DatasetDefinition)


def log_dataset(name, definition, run=None):
    from .dataprep_utilities import is_dataflow
    try:
        if (is_dataset(definition) or is_dataflow(definition)) and _contains_dataset_ref(definition):
            run = run or Run.get_context()
            run.log(name=name, value=_get_dataset_info(definition))
    except Exception as e:
        module_logger.warning('Unable to log dataset.\nException: {}'.format(e))


def convert_inputs(X, y, X_valid, y_valid):
    return tuple(_convert_to_trackable_definition(dataset) for dataset in [X, y, X_valid, y_valid])


def _convert_to_trackable_definition(dataset):
    if not _azureml_core_installed:
        module_logger.debug('Unable to convert input to trackable definition')
        return dataset

    definition, trackable = _reference_dataset(dataset)
    if not trackable:
        module_logger.debug('Unable to convert input to trackable definition')
    return definition


def _reference_dataset(dataset):
    from azureml.dataprep import Dataflow

    if not is_dataset(dataset) and not isinstance(dataset, Dataflow):
        return dataset, False

    if type(dataset) == Dataflow:
        return dataset, _contains_dataset_ref(dataset)

    # un-registered dataset
    if isinstance(dataset, DatasetDefinition) and not dataset._workspace:
        return dataset, _contains_dataset_ref(dataset)

    _verify_dataset(dataset)
    return Dataflow.reference(dataset), True


def _contains_dataset_ref(definition):
    for step in definition._get_steps():
        if step.step_type == 'Microsoft.DPrep.ReferenceBlock' \
                and _get_ref_container_path(step).startswith('dataset://'):
            return True
    return False


def _get_dataset_info(definition):
    for step in definition._get_steps():
        ref_path = _get_ref_container_path(step)
        if step.step_type == 'Microsoft.DPrep.ReferenceBlock' and ref_path.startswith('dataset://'):
            return ref_path
    raise DataprepException('Unexpected error, unable to retrieve dataset information.')


def _get_ref_container_path(step):
    if step.step_type != 'Microsoft.DPrep.ReferenceBlock':
        return ''
    try:
        return step.arguments['reference'].reference_container_path or ''
    except AttributeError:
        # this happens when a dataflow is serialized and deserialized
        return step.arguments['reference']['referenceContainerPath'] or ''
    except KeyError:
        return ''


def _verify_dataset(dataset):
    if isinstance(dataset, Dataset):
        if dataset.state == _deprecated:
            module_logger.warning('Warning: dataset \'{}\' is deprecated.'.format(dataset.name))
        if dataset.state == _archived:
            message = 'Error: dataset \'{}\' is archived and cannot be used.'.format(dataset.name)
            ex = ValueError(message)
            logging_utilities.log_traceback(
                ex,
                module_logger
            )
            raise ex
    if isinstance(dataset, DatasetDefinition):
        if dataset._state == _deprecated:
            message = 'Warning: this definition is deprecated.'
            dataset_and_version = ''
            if dataset._deprecated_by_dataset_id:
                dataset_and_version += 'Dataset ID: \'{}\' '.format(dataset._deprecated_by_dataset_id)
            if dataset._deprecated_by_definition_version:
                dataset_and_version += 'Definition version: \'{}\' '.format(dataset._deprecated_by_definition_version)
            if dataset_and_version:
                message += ' Please use \'{}\' instead.'.format(dataset_and_version.strip(' '))
            module_logger.warning(message)
        if dataset._state == _archived:
            message = 'Error: definition version \'{}\' is archived and cannot be used'.format(dataset._version_id)
            ex = ValueError(message)
            logging_utilities.log_traceback(
                ex,
                module_logger
            )
            raise ex
