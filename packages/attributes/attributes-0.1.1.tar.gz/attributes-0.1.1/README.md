# attributes

![GitHub](https://img.shields.io/github/license/Cologler/attributes-python.svg)
[![Build Status](https://travis-ci.com/Cologler/attributes-python.svg?branch=master)](https://travis-ci.com/Cologler/click-anno-python)
[![PyPI](https://img.shields.io/pypi/v/attributes.svg)](https://pypi.org/project/attributes/)

a python version attribute like attribute of csharp.

## Usage

``` py
from attributes import Attribute

class Data(Attribute): # make your own attribute
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

@Data(1, 2) # use your attribute
class SomeClass:
    pass

data, = Attribute.get_attrs(SomeClass) # than load on runtime and use it.
```

### Parameter Attribute

``` py
@param_attr('a', Data(1, 2), Data(3, 4))
def func(a):
    pass

data, = Attribute.get_attrs(param_of(func, 'a'))
# or
data, = Data.get_from_param(func, 'a')
```
