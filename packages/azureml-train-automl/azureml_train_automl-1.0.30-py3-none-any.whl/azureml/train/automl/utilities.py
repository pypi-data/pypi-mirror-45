# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods used by automated machine learning."""
from typing import Union
from automl.client.core.common import utilities as common_utilities
from automl.client.core.common.exceptions import AutoMLException
from azureml.exceptions import ServiceException as AzureMLServiceException
from msrest.exceptions import HttpOperationError

from . import _constants_azureml


def friendly_http_exception(exception: Union[AzureMLServiceException, HttpOperationError], api_name: str) -> None:
    """
    Friendly exceptions for a http exceptions.

    :param exception: exception raised from a network call.
    :param api_name: name of the API call made.
    :raise: AutoMLException
    """
    try:
        if isinstance(exception, HttpOperationError):
            status_code = exception.error.response.status_code

            # Raise bug with msrest team that response.status_code is always 500
            if status_code == 500:
                try:
                    message = exception.message
                    substr = 'Received '
                    substr_idx = message.find(substr) + len(substr)
                    status_code = int(message[substr_idx:substr_idx + 3])
                except Exception:
                    pass
        else:
            status_code = exception.status_code
    except Exception:
        raise exception.with_traceback(exception.__traceback__)

    if status_code in _constants_azureml.HTTP_ERROR_MAP:
        http_error = _constants_azureml.HTTP_ERROR_MAP[status_code]
    else:
        http_error = _constants_azureml.HTTP_ERROR_MAP['default']
    if api_name in http_error:
        error_message = http_error[api_name]
    elif status_code == 400:
        # 400 bad request could be basically anything. Just pass the original exception message through
        error_message = exception.message
    else:
        error_message = http_error['default']
    raise AutoMLException(
        "{0} error raised. {1}".format(http_error['Name'], error_message), http_error['type']
    ).with_traceback(exception.__traceback__) from exception


def get_primary_metrics(task):
    """
    Get the primary metrics supported for a given task as a list.

    :param task: string "classification" or "regression".
    :return: A list of the primary metrics supported for the task.
    """
    return common_utilities.get_primary_metrics(task)


def _get_package_version():
    """
    Get the package version string.

    :return: The version string.
    """
    from . import __version__
    return __version__
