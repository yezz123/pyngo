import warnings
from collections import deque
from typing import Any, Dict, Type, TypeVar, get_origin

import typing_extensions
from django.http import QueryDict
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.warnings import PydanticDeprecatedSince20

_QueryDictModel = TypeVar("_QueryDictModel", bound="QueryDictModel")


class QueryDictModel(BaseModel):
    """
    A model that can be initialized from a QueryDict.

    This is a base class for models that can be initialized from a QueryDict.

    The QueryDictModel class is a base class for models that can be initialized

    from a QueryDict.
    """

    @classmethod
    def model_validate(
        cls: type[_QueryDictModel],
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> "_QueryDictModel":
        """
        Parse a QueryDict into a model.

        Returns:
            A model that was initialized from the QueryDict.
        """
        if isinstance(obj, QueryDict):
            obj = querydict_to_dict(obj, cls)
        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)

    @classmethod
    @typing_extensions.deprecated(
        "The `parse_obj` method is deprecated; use `model_validate` instead.", category=PydanticDeprecatedSince20
    )
    def parse_obj(cls: type["_QueryDictModel"], obj: Any) -> "_QueryDictModel":  # noqa: D102
        warnings.warn(
            "The `parse_obj` method is deprecated; use `model_validate` instead.", DeprecationWarning, stacklevel=2
        )
        return cls.model_validate(obj)


def querydict_to_dict(
    query_dict: QueryDict,
    model_class: Type[BaseModel],
) -> Dict[str, Any]:
    """
    Convert a QueryDict into a dictionary.

    Args:
        query_dict (QueryDict): The QueryDict to convert.
        model_class (Type[BaseModel]): The model class to use for the conversion.

    Returns:
        Dict[str, Any]: The converted dictionary.
    """
    to_dict: Dict[str, Any] = {}
    model_fields = model_class.model_fields

    for key, orig_value in query_dict.items():
        # Get field name (as defined in Pydantic model, not necessary the key in data dict, because of aliasing)
        field_key = next((name for (name, inf) in model_fields.items() if inf.alias == key), key)

        if field_key not in model_fields:
            to_dict[key] = orig_value
            continue
        field = model_fields[field_key]
        # Discard field if its value is empty string and we don't expect string in model
        if orig_value in ("", b"") and not _is_string_like_field(field):
            continue
        if _is_sequence_field(field):
            to_dict[key] = query_dict.getlist(key)
        else:
            to_dict[key] = query_dict.get(key)
    return to_dict


def _is_string_like_field(field: FieldInfo) -> bool:
    """
    Check if a field is a string-like field (str, bytes, bytearray, StrEnum).

    Args:
        field (FieldInfo): The field to check.

    Returns:
        bool: True if the field is a string-like field, False otherwise.
    """
    if not field.annotation:
        return False
    try:
        return issubclass(field.annotation, (str, bytes, bytearray))
    except TypeError:
        return False


def _is_sequence_field(field: FieldInfo) -> bool:
    """
    Check if a field is a list field.

    Args:
        field (FieldInfo): The field to check.

    Returns:
        bool: True if the field is a list field, False otherwise.
    """
    origin_type = get_origin(field.annotation)
    return origin_type in (list, tuple, deque, set, frozenset)
