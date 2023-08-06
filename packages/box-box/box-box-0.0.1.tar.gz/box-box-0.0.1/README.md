# box [![Build Status](https://travis-ci.com/FebruaryBreeze/box.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/box) [![codecov](https://codecov.io/gh/FebruaryBreeze/box/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/box) [![PyPI version](https://badge.fury.io/py/box.svg)](https://pypi.org/project/box/)

Box of Python Class and Object

## Installation

Need Python 3.6+.

```bash
pip install box
```

## Usage

```python
import box


@box.register
class CustomModule:
    @classmethod
    def factory(cls, config):
        return cls()

# 1. load class from name
obj_class = box.load('CustomModule')
obj = obj_class()

# 2. object factory from config
obj = box.factory(config={
    'type': 'CustomModule'
})
```
