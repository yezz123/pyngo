from typing import List, Type, cast

from pydantic import BaseModel
from pydantic.fields import ModelField
from typing_extensions import Literal, TypedDict

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


def openapi_params(
    model_class: Type[BaseModel],
) -> List[ParameterDict]:
    parameters: List[ParameterDict] = []

    for field in model_class.__fields__.values():
        if field.is_complex():
            raise ValueError("Only simple types allowed")
        else:
            parameters.append(_pydantic_field_to_parameter(field))

    return parameters


def _pydantic_field_to_parameter(field: ModelField) -> ParameterDict:
    location = field.field_info.extra.get("location", "query")
    if location not in _VALID_LOCATIONS:
        raise ValueError(f"location must be one of: {', '.join(_VALID_LOCATIONS)}")

    required = field.required
    if location == "path" and not required:
        raise ValueError("Path parameters must be required")

    field_extra = field.field_info.extra
    deprecated = field_extra.get("deprecated", False)

    args = {
        "name": field.name,
        "in": location,
        "description": field.field_info.description or "",
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
