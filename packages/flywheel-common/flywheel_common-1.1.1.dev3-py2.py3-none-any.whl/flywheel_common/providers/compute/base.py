"""Provides the BaseProvider base class"""
import copy
from abc import ABCMeta, abstractmethod

from ..provider import BaseProvider
from ... import errors

class BaseComputeProvider(BaseProvider):
    """The base compute provider object. Provides configuration and validation interface for compute types"""
    # For automatic plugin registration
    __metaclass__ = ABCMeta

    # The schema for validating configuration (required)
    _schema = None

    # The set of confidential fields (required)
    confidential_fields = None


