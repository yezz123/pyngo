from typing import Dict, Optional

import pytest
from pydantic import BaseModel, Field

from pyngo import ParameterDict, openapi_params


class TestPydanticModelToOpenapiParameters:
    def test_only_primitive_types_allowed(self) -> None:
        class Model(BaseModel):
            non_primitive: Dict[str, str]

        with pytest.raises(ValueError) as exc:
            openapi_params(Model)
        assert str(exc.value) == "Only simple types allowed"

    def test_prohibits_unknown_location(self) -> None:
        class Model(BaseModel):
            path_param: int = Field(json_schema_extra={"location": "foo"})

        with pytest.raises(ValueError) as exc:
            openapi_params(Model)
        assert str(exc.value) == "location must be one of: query, header, path, cookie"

    def test_prohibits_optional_path_params(self) -> None:
        class Model(BaseModel):
            path_param: Optional[int] = Field(default=0, json_schema_extra={"location": "path"})

        with pytest.raises(ValueError) as exc:
            openapi_params(Model)
        assert str(exc.value) == "Path parameters must be required"

    def test_defaults_path_params_to_be_required(self) -> None:
        class Model(BaseModel):
            path_param: int = Field(json_schema_extra={"location": "path"})

        params = openapi_params(Model)
        assert len(params) == 1
        assert params[0]["required"]

    @pytest.mark.parametrize("param_loc", ("header", "path", "cookie"))
    def test_prohibits_allow_empty_outside_of_query(self, param_loc: str) -> None:
        class Model(BaseModel):
            param: int = Field(json_schema_extra={"location": param_loc, "allowEmptyValue": True})

        with pytest.raises(ValueError) as exc:
            openapi_params(Model)
        assert str(exc.value) == "allowEmptyValue only permitted for 'query' values"

    def test_allow_empty_excluded_for_non_query_params(self) -> None:
        class Model(BaseModel):
            param: int = Field(json_schema_extra={"location": "header"})

        params = openapi_params(Model)
        assert len(params) == 1
        assert "allowEmptyValue" not in params[0]

    def test_allow_empty_value_defaults_to_true_for_query_params(self) -> None:
        class Model(BaseModel):
            param: int = Field()

        self.openapi_param(Model, "allowEmptyValue")

    def test_deprecated_defaults_to_false(self) -> None:
        class Model(BaseModel):
            param: int = Field()

        self.openapi_param(Model, "deprecated")

    def test_optional_fields_are_not_required(self) -> None:
        class Model(BaseModel):
            param: Optional[int] = Field(default=0)

        self.openapi_param(Model, "required")

    def openapi_param(self, Model, arg):
        params = openapi_params(Model)
        assert len(params) == 1
        assert not params[0][arg]

    def test_reading_query_params(self) -> None:
        class PathParams(BaseModel):
            document_id: int = Field(
                description="The document id",
                json_schema_extra={
                    "location": "query",
                    "deprecated": True,
                    "allowEmptyValue": True,
                },
            )

        expected_parameters = [
            ParameterDict(
                {
                    "in": "query",
                    "name": "document_id",
                    "description": "The document id",
                    "required": True,
                    "deprecated": True,
                    "allowEmptyValue": True,
                }
            )
        ]

        assert openapi_params(PathParams) == expected_parameters
