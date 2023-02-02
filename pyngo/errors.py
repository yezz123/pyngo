from typing import Any, Dict, Sequence

from pydantic import ValidationError


def drf_error_details(exception: ValidationError) -> Dict[str, Any]:
    """
    Convert a pydantic ValidationError into a DRF-style error response.

    Args:
        exception (ValidationError): The exception to convert.

    Returns:
        Dict[str, Any]: The error response.
    """
    drf_data: Dict[str, Any] = {}
    for error in exception.errors():
        set_nested(drf_data, error["loc"], [error["msg"]])  # type: ignore
    return drf_data


def set_nested(data: Dict[str, Any], keys: Sequence[str], value: Any) -> None:
    """
    Set a value in a nested dictionary.

    Args:
        data (Dict[str, Any]): The dictionary to set the value in.
        keys (Sequence[str]): The keys to set the value at.
        value (Any): The value to set.

    Returns:
        None
    """
    for key in keys[:-1]:
        data = data.setdefault(str(key), {})
    data[keys[-1]] = value


def get_nested(data: Dict[str, Any], keys: Sequence[str]) -> Any:
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
