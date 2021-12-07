import sys
from typing import Any, Dict, List, Optional, Type, TypeVar

from django.http import QueryDict
from pydantic import BaseModel
from pydantic.fields import ModelField

if sys.version_info >= (3, 8):
    from typing import get_origin
else:

    def get_origin(tp: Any) -> Optional[Any]:
        try:
            return tp.__origin__
        except AttributeError:
            return None


_QueryDictModel = TypeVar("_QueryDictModel", bound="QueryDictModel")


class QueryDictModel(BaseModel):
    """
    A model that can be initialized from a QueryDict.

    This is a base class for models that can be initialized from a QueryDict.

    The QueryDictModel class is a base class for models that can be initialized

    from a QueryDict.
    """

    @classmethod
    def parse_obj(cls: Type["_QueryDictModel"], obj: Any) -> "_QueryDictModel":
        """
        Parse a QueryDict into a model.

        Returns:
            A model that was initialized from the QueryDict.
        """
        if isinstance(obj, QueryDict):
            obj = querydict_to_dict(obj, cls)
        return super().parse_obj(obj)


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
    model_fields = model_class.__fields__

    for key in query_dict.keys():
        if key in model_fields and _is_list_field(model_fields[key]):
            to_dict[key] = query_dict.getlist(key)
        else:
            to_dict[key] = query_dict.get(key)
    return to_dict


def _is_list_field(field: ModelField) -> bool:
    """
    Check if a field is a list field.

    Args:
        field (ModelField): The field to check.

    Returns:
        bool: True if the field is a list field, False otherwise.
    """
    if sys.version_info >= (3, 7):
        return get_origin(field.outer_type_) == list
    else:
        return get_origin(field.outer_type_) == List
