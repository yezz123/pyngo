# Pyngo :snake:

<p align="center">
    <em>Utils to help integrate pydantic into Django projects</em>
</p>

[![Downloads](https://pepy.tech/badge/pyngo)](https://pepy.tech/project/pyngo)
[![codecov](https://codecov.io/gh/yezz123/pyngo/branch/main/graph/badge.svg)](https://codecov.io/gh/yezz123/pyngo)
[![PyPI version](https://badge.fury.io/py/pyngo.svg)](https://badge.fury.io/py/pyngo)
[![framework](https://img.shields.io/badge/Framework-Django-green?style)](https://www.djangoproject.com/)
[![Pypi](https://img.shields.io/pypi/pyversions/pyngo.svg?color=%2334D058)](https://pypi.org/project/pyngo)

---

**Install the project**: `pip install pyngo`

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

- We use [Flit](https://flit.readthedocs.io/) as a dependency manager, thats why we need to setup it before installing all requirements of development and testing.

```sh
pip install flit
```

- Now we can install dependencies for development and testing.

```sh
flit install --symlink
```

### Test the code 📚

For Building the tests i use `pytest`, you can run it using a pre-configured command:

```bash
make test
```

### Format the code 💅

Execute the following command to apply `pre-commit` formatting:

```bash
make lint
```

## License 🍻

This project is licensed under the terms of the MIT license.
