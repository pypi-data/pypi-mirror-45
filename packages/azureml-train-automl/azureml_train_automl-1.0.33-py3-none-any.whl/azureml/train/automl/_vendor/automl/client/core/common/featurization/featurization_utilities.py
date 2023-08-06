# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for featurizers."""
from typing import Any, Callable, List, Optional, TypeVar
import importlib

from automl.client.core.common import logging_utilities
from .automltransformer import AutoMLTransformer


ReturnFeaturizerT = TypeVar('ReturnFeaturizerT', bound=AutoMLTransformer)


def if_package_exists(feature_name: str, packages: List[str]) \
        -> 'Callable[..., Callable[..., Optional[ReturnFeaturizerT]]]':
    """
    Check if package is installed.

    If exists then make call to the function wrapped.
    Else log the error and return None.

    :param feature_name: Feature name that wil be enabled or disabled based on packages availability.
    :type feature_name: str.
    :param packages: Packages to check
    :type packages: List of packages.
    :return: Wrapped function call.
    """
    def func_wrapper(function: 'Callable[..., ReturnFeaturizerT]') -> 'Callable[..., Optional[ReturnFeaturizerT]]':

        def f_wrapper(*args: Any, **kwargs: Any) -> Optional[ReturnFeaturizerT]:
            package = None
            try:
                for package in packages:
                    importlib.import_module(name=package)
                return function(*args, **kwargs)

            except ImportError as e:
                logger = logging_utilities.get_logger()
                logger.warning(
                    "'{}' package not found, '{}' will be disabled. Exception: {}".format(package, feature_name, e))
                return None

        return f_wrapper

    return func_wrapper
