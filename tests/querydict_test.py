import os
from typing import Any, Dict, List, Optional, Union

import pytest
from django.http import QueryDict
from pydantic import BaseModel

from pyngo import QueryDictModel

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


class Model(QueryDictModel, BaseModel):
    foo: int
    bar: List[int]
    sub_id: Optional[int]
    key: str = "key"


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        (QueryDict("foo=12&bar=12"), Model(foo=12, bar=[12], key="key")),
        ({"foo": 44, "bar": [0, 4]}, Model(foo=44, bar=[0, 4], key="key")),
        (
            QueryDict("foo=10&bar=12&sub_id=&key="),
            Model(foo=10, bar=[12], sub_id=None, key=""),
        ),
        (
            QueryDict("foo=10&bar=12&key=abc&extra=something"),
            Model(foo=10, bar=[12], key="abc"),
        ),
    ),
)
def test_parsing_objects(
    data: Union[QueryDict, Dict[str, Any]], expected: Model
) -> None:
    got = Model.parse_obj(data)
    assert got == expected
    assert got.foo == expected.foo
    assert got.bar == expected.bar
    assert got.sub_id == expected.sub_id
    assert got.key == expected.key
