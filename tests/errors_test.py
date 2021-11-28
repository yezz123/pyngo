from typing import List, Optional

from pydantic import BaseModel, ValidationError, validator

from pyngo import drf_error_details


class NestedModel(BaseModel):
    str_field: str

    @validator("str_field")
    def must_be_bar(cls, value: str) -> str:
        special_name = "bar"
        if value != special_name:
            raise ValueError(f"Name must be: '{special_name}'!")
        else:
            return value


class MyModel(BaseModel):
    int_field: Optional[int]
    nested_field: Optional[NestedModel]
    nested_list: Optional[List[NestedModel]]

    @validator("int_field")
    def must_be_special_value(cls, value: int) -> int:
        magic_number = 42
        if value != magic_number:
            raise ValueError("Must be the magic number!")
        else:
            return value


class TestToDRFError:
    def test_with_single_flat_field(self) -> None:
        try:
            MyModel(int_field=2)
        except ValidationError as e:
            assert drf_error_details(e) == {"int_field": ["Must be the magic number!"]}

    def test_with_nested_field(self) -> None:
        try:
            MyModel.parse_obj({"int_field": 42, "nested_field": {"str_field": "foo"}})
        except ValidationError as e:
            assert drf_error_details(e) == {
                "nested_field": {"str_field": ["Name must be: 'bar'!"]}
            }

    def test_with_nested_list(self) -> None:
        try:
            MyModel.parse_obj(
                {"nested_list": [{"str_field": "bar"}, {"str_field": "foo"}]}
            )
        except ValidationError as e:
            assert drf_error_details(e) == {
                "nested_list": {"1": {"str_field": ["Name must be: 'bar'!"]}}
            }
