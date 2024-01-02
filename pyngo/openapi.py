import types
from typing import List, Literal, Optional, Type, TypedDict, Union, cast, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

_In = Literal["query", "header", "path", "cookie"]

ParameterDict = TypedDict(
    "ParameterDict",
    {
        "name": str,
        "in": _In,
        "description": str,
        "required": bool,
        "deprecated": bool,
        "allowEmptyValue": bool,
    },
    total=False,
)

_VALID_LOCATIONS = ("query", "header", "path", "cookie")


def is_simple_type(field: FieldInfo) -> bool:
    """
    Returns True if the given field has simple type.

    Args:
        field (FieldInfo): The field to check.

    Returns:
        bool: True if the given field has simple type.
    """
    args = get_args(field.annotation)
    if args == ():
        return True
    origin = get_origin(field.annotation)
    if origin in [Optional, Union]:
        match args:
            case (klass, types.NoneType) if get_args(klass) == ():
                return True
            case (types.NoneType, klass) if get_args(klass) == ():
                return True
            case _:
                return False
    return False


def openapi_params(
    model_class: Type[BaseModel],
) -> List[ParameterDict]:
    """
    Returns a list of parameters for the given model class.

    Args:
        model_class (Type[BaseModel]): The model class to get parameters for.

    Raises:
        ValueError: If the model class is not a pydantic model.
        ValueError: If the model class has a field with an invalid location.
        ValueError: If the model class has a field with allowEmptyValue set for a location other than 'query'.
        ValueError: If the model class has a field with required set to False for a path parameter.

    Returns:
        List[ParameterDict]: A list of parameters for the given model class.
    """
    parameters: List[ParameterDict] = []

    for name, field in model_class.model_fields.items():
        if not is_simple_type(field):
            raise ValueError("Only simple types allowed")
        parameters.append(_pydantic_field_to_parameter(name, field))

    return parameters


def _pydantic_field_to_parameter(name: str, field: FieldInfo) -> ParameterDict:
    """
    Converts a pydantic field to an OpenAPI parameter.

    Args:
        field (FieldInfo): The field to convert.

    Raises:
        ValueError: If the field has an invalid location.
        ValueError: If the field has allowEmptyValue set for a location other than 'query'.
        ValueError: If the field has required set to False for a path parameter.

    Returns:
        ParameterDict: The converted field.
    """
    field_extra = (None if callable(field.json_schema_extra) else field.json_schema_extra) or {}
    location = field_extra.get("location", "query")
    if location not in _VALID_LOCATIONS:
        raise ValueError(f"location must be one of: {', '.join(_VALID_LOCATIONS)}")

    required = field.is_required()
    if location == "path" and not required:
        raise ValueError("Path parameters must be required")

    deprecated = field_extra.get("deprecated", False)

    args = {
        "name": name,
        "in": location,
        "description": field.description or "",
        "required": required,
        "deprecated": deprecated,
    }
    allow_empty_value = field_extra.get("allowEmptyValue")
    if allow_empty_value is not None and location != "query":
        raise ValueError("allowEmptyValue only permitted for 'query' values")
    elif location == "query":
        if allow_empty_value is not None:
            args["allowEmptyValue"] = allow_empty_value
        else:
            args["allowEmptyValue"] = False

    return cast(ParameterDict, args)
