from collections.abc import Sequence
from typing import Any

from pydantic import ValidationError


def drf_error_details(exception: ValidationError) -> dict[str, Any]:
    """
    Convert a pydantic ValidationError into a DRF-style error response.

    Args:
        exception (ValidationError): The exception to convert.

    Returns:
        dict[str, Any]: The error response.
    """
    drf_data: dict[str, Any] = {}
    for error in exception.errors():
        set_nested(drf_data, error["loc"], [error["msg"]])
    return drf_data


def set_nested(data: dict[str, Any], keys: Sequence[int | str], value: Any) -> None:
    """
    Set a value in a nested dictionary.

    Args:
        data (dict[str, Any]): The dictionary to set the value in.
        keys (tuple[int | str, ...]): The keys to set the value at.
        value (Any): The value to set.

    Returns:
        None
    """
    for key in keys[:-1]:
        data = data.setdefault(str(key), {})
    data[str(keys[-1])] = value


def get_nested(data: dict[str, Any], keys: Sequence[str]) -> Any:
    """
    Get a value from a nested dictionary.

    Args:
        data (Dict[str, Any]): The dictionary to get the value from.
        keys (Sequence[str]): The keys to get the value at.

    Returns:
        Any: The value.
    """
    for key in keys[:-1]:
        data = data[key]
    return data[keys[-1]]
