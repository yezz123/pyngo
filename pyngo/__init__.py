"""Pydantic Package for Adding Models into a Django or Django Rest Framework Project"""

__version__ = "2.0.1"

from .errors import drf_error_details
from .openapi import ParameterDict, openapi_params
from .querydict import QueryDictModel, querydict_to_dict

__all__ = (
    "ParameterDict",
    "QueryDictModel",
    "querydict_to_dict",
    "drf_error_details",
    "openapi_params",
)
