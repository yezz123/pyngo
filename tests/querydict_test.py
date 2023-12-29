import os
from collections import deque
from typing import Any, Deque, Dict, FrozenSet, List, Optional, Tuple, Union

import pytest
from django.http import QueryDict
from pydantic import BaseModel, Field

from pyngo import QueryDictModel

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


class Model(QueryDictModel, BaseModel):
    foo: int
    bar: List[int]
    sub_id: Optional[int] = None
    key: str = "key"
    wings: Tuple[int, ...] = Field(default_factory=tuple)
    queue: Deque[int] = Field(default_factory=deque)
    basket: FrozenSet[int] = Field(default_factory=frozenset)
    alias_list: List[int] = Field(alias="alias[list]", default_factory=list)


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        (
            QueryDict("foo=12&bar=12"),
            Model(foo=12, bar=[12], key="key", wings=(), queue=deque(), basket=frozenset()),
        ),
        ({"foo": 44, "bar": [0, 4]}, Model(foo=44, bar=[0, 4], key="key")),
        (
            QueryDict("foo=10&bar=12&sub_id=&key="),
            Model(foo=10, bar=[12], sub_id=None, key=""),
        ),
        (
            QueryDict("foo=10&bar=12&key=abc&extra=something"),
            Model(foo=10, bar=[12], key="abc"),
        ),
        (
            QueryDict("foo=8&bar=9&wings=1&wings=2&queue=3&queue=4"),
            Model(foo=8, bar=[9], wings=(1, 2), queue=deque((3, 4))),
        ),
        (
            QueryDict("foo=8&bar=9&basket=5&basket=6"),
            Model(foo=8, bar=[9], basket=frozenset((5, 6))),
        ),
        (
            QueryDict("foo=8&bar=9&basket=5&basket=6&alias[list]=5&alias[list]=3"),
            # This has to  be a dictionary due to the invalid characters in alias[list]
            # Which has to be set because that's what the model is looking for via the Field alias
            Model(
                **{
                    "foo": 8,
                    "bar": [9],
                    "basket": frozenset((5, 6)),
                    "alias[list]": [5, 3],
                }
            ),
        ),
    ),
)
def test_parsing_objects(data: Union[QueryDict, Dict[str, Any]], expected: Model) -> None:
    got = Model.model_validate(data)
    assert got == expected
    assert got.foo == expected.foo
    assert got.bar == expected.bar
    assert got.sub_id == expected.sub_id
    assert got.key == expected.key
    assert got.wings == expected.wings
    assert got.queue == expected.queue
    assert got.basket == expected.basket
    assert got.alias_list == expected.alias_list
