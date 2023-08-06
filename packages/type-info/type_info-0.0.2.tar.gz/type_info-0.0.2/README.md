# type-info

![GitHub](https://img.shields.io/github/license/Cologler/type-info-python.svg)
[![Build Status](https://travis-ci.com/Cologler/type-info-python.svg?branch=master)](https://travis-ci.com/Cologler/type-info-python)
[![PyPI](https://img.shields.io/pypi/v/type-info.svg)](https://pypi.org/project/type-info/)

Provide some oop api for `typing` module.

Support python 3.6+, tested on `3.6` and `3.7`.

## Usage

``` py
from type_info import get_type_info

type_info = get_type_info(typing.Dict[str, int])
assert type_info.generic_type is typing.Dict
assert type_info.generic_args == (str, int)
assert type_info.dynamic_type is dict
```

read unittests for more examples.
