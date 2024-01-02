from typing import List, Optional

import pytest
from pydantic import BaseModel, ValidationError, field_validator

from pyngo import drf_error_details
from pyngo.errors import get_nested


class NestedModel(BaseModel):
    str_field: str

    @field_validator("str_field")
    @classmethod
    def must_be_bar(cls, value: str) -> str:
        special_name = "bar"
        if value != special_name:
            raise ValueError(f"Name must be: '{special_name}'!")
        else:
            return value


class MyModel(BaseModel):
    int_field: Optional[int] = None
    nested_field: Optional[NestedModel] = None
    nested_list: Optional[List[NestedModel]] = None

    @field_validator("int_field")
    @classmethod
    def must_be_special_value(cls, value: int) -> int:
        magic_number = 42
        if value != magic_number:
            raise ValueError("Must be the magic number!")
        else:
            return value


class TestToDRFError:
    def test_with_single_flat_field(self) -> None:
        with pytest.raises(ValidationError) as e:
            MyModel(int_field=2)
        assert drf_error_details(e.value) == {"int_field": ["Value error, Must be the magic number!"]}

    def test_with_nested_field(self) -> None:
        with pytest.raises(ValidationError) as e:
            MyModel(nested_field={"str_field": "foo"})
        assert drf_error_details(e.value) == {"nested_field": {"str_field": ["Value error, Name must be: 'bar'!"]}}

    def test_with_nested_list(self) -> None:
        try:
            MyModel.model_validate({"nested_list": [{"str_field": "bar"}, {"str_field": "foo"}]})
        except ValidationError as e:
            assert drf_error_details(e) == {"nested_list": {"1": {"str_field": ["Value error, Name must be: 'bar'!"]}}}


class TestGetNested:
    def test_get_nested_with_valid_data(self):
        result = self.data("bar")
        # Assert the result
        assert result == "bar"

    def test_get_nested_with_invalid_data(self):
        result = self.data("not_bar")
        with pytest.raises(ValueError, match="Name must be: 'bar'!"):
            NestedModel(str_field=result).model_dump()

    def data(self, arg):
        nested_data = {"first": {"second": {"third": {"str_field": arg}}}}
        keys = ["first", "second", "third", "str_field"]
        return get_nested(nested_data, keys)

    def test_must_be_bar_validator_with_valid_value(self):
        # Create a valid NestedModel instance
        valid_model = NestedModel(str_field="bar")

        # Assert that validation does not raise an error
        valid_model.model_dump()

    def test_must_be_bar_validator_with_invalid_value(self):
        # Create an invalid NestedModel instance
        with pytest.raises(ValidationError, match="Name must be: 'bar'!"):
            NestedModel(str_field="not_bar")


class TestMyModel:
    def test_must_be_special_value_validator_with_invalid_value(self):
        with pytest.raises(ValidationError, match="Must be the magic number!"):
            MyModel(int_field=10)

    def test_valid_model_creation(self):
        valid_model = MyModel(int_field=42, nested_field=NestedModel(str_field="bar"))
        assert valid_model.int_field == 42
        assert valid_model.nested_field.str_field == "bar"
