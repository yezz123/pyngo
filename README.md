# Pyngo :snake:

<p align="center">
    <em>Utils to help integrate pydantic into Django projects</em>
</p>

<p align="center">
<a href="https://github.com/yezz123/pyngo/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/yezz123/pyngo/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/yezz123/pyngo">
    <img src="https://codecov.io/gh/yezz123/pyngo/branch/main/graph/badge.svg"/>
</a>
<a href="https://pypi.org/project/pyngo" target="_blank">
    <img src="https://img.shields.io/pypi/v/pyngo?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pyngo" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pyngo.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

## Installation

You can add pyngo in a few easy steps. First of all, install the dependency:

```sh
$ pip install pyngo

---> 100%

Successfully installed pyngo
```

---

## Features 🎉

- Using Pydantic to Build your Models in Django Project.
- Using `OpenAPI` utilities to build params from a basic model.
- using `QueryDictModel` to build `Pydantic` models from a `QueryDict` object.
- propagate any errors from Pydantic in Django Rest Framework.
- Tested in Python 3.6 and up.

## Examples 📚

### OpenAPI

- `pyngo.openapi_params()` can build params from a basic model

```py
from pydantic import BaseModel
from pyngo import openapi_params

class Model(BaseModel):
   bingo: int

print(openapi_params(Model))
```

- `pyngo.ParameterDict.required` is set according to the type of the variable

```py
from typing import Optional
from pydantic import BaseModel
from pyngo import openapi_params

class Model(BaseModel):
   required_param: int
   optional_param: Optional[int]

print(openapi_params(Model))
```

Other fields can be set through the field’s info:

```py
from pydantic import BaseModel, Field
from pyngo import openapi_params

class WithDescription(BaseModel):
   described_param: str = Field(
      description="Hello World Use Me!"
   )

class InPath(BaseModel):
   path_param: str = Field(location="path")

class WithDeprecated(BaseModel):
   deprecated_field: bool = Field(deprecated=True)

class WithNoAllowEmpty(BaseModel):
   can_be_empty: bool = Field(allowEmptyValue=False)

print(openapi_params(WithDescription)[0]["description"])
print(openapi_params(InPath)[0]["in"])
print(openapi_params(WithDeprecated)[0]["deprecated"])
print(openapi_params(WithNoAllowEmpty)[0]["allowEmptyValue"])
```

### Django

- `pyngo.querydict_to_dict()` and `pyngo.QueryDictModel` are conveniences for building a `pydantic.BaseModel` from a `django.QueryDict`.

```py
from typing import List
from django.http import QueryDict
from pydantic import BaseModel
from pyngo import QueryDictModel, querydict_to_dict

class Model(BaseModel):
   single_param: int
   list_param: List[str]

class QueryModel(QueryDictModel):
   single_param: int
   list_param: List[str]

query_dict = QueryDict("single_param=20&list_param=Life")

print(Model.parse_obj(querydict_to_dict(query_dict, Model)))
print(QueryModel.parse_obj(query_dict))
```

> **Note:** Don't forget to Setup the Django Project.

### Django Rest Framework

- `pyngo.drf_error_details()` will propagate any errors from Pydantic.

```py
from pydantic import BaseModel, ValidationError
from pyngo import drf_error_details

class Model(BaseModel):
   foo: int
   bar: str

data = {"foo": "Cat"}

try:
   Model.parse_obj(data)
except ValidationError as e:
   print(drf_error_details(e))
```

Errors descend into nested fields:

```py
from typing import List
from pydantic import BaseModel, ValidationError
from pyngo import drf_error_details

class Framework(BaseModel):
   frm_id: int

class Language(BaseModel):
   framework: List[Framework]

data = {"Framework": [{"frm_id": "not_a_number"}, {}]}
expected_details = {
   "framework": {
      "0": {"frm_id": ["value is not a valid integer"]},
      "1": {"frm_id": ["field required"]},
   }
}

try:
   Framework.parse_obj(data)
except ValidationError as e:
   print(drf_error_details(e))
```

## Development 🚧

### Setup environment 📦

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
# Install dependencies
pip install -e .[test,lint]
```

### Run tests 🌝

You can run all the tests with:

```bash
bash scripts/test.sh
```

> Note: You can also generate a coverage report with:

```bash
bash scripts/test_html.sh
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
bash scripts/format.sh
```

Execute the following command to apply `mypy` type checking:

```bash
bash scripts/lint.sh
```

## License 🍻

This project is licensed under the terms of the MIT license.
