# halerror
> The best python exception library

[![PyPI](https://img.shields.io/pypi/v/halerror.svg)](https://pypi.org/project/halerror/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/halerror.svg)](https://pypi.org/project/halerror/)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Documentation Status](https://readthedocs.org/projects/halerror/badge/?version=latest)](https://halerror.readthedocs.io/en/latest/)
[![Travis (.org)](https://img.shields.io/travis/jmp1985/halerror.svg)](https://travis-ci.org/jmp1985/halerror)
[![Codecov](https://img.shields.io/codecov/c/github/jmp1985/halerror.svg)](https://codecov.io/gh/jmp1985/halerror)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jmp1985/halerror.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jmp1985/halerror/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/jmp1985/halerror.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jmp1985/halerror/alerts/)

This python library implements a sci-fi exception class!

## Installation

The package is available from [PyPI](https://pypi.org/project/halerror/0.4.0/).
To install using pip, do the following:

```sh
pip install halerror
```

To install from source, clone this repository and then do the following:

```sh
python setup.py install
```

## Testing

To run the tests, clone this repository and the do the following:

```sh
python setup.py test
```

## Building the documentation

To build the documenation, clone this repository and the do the following:

```sh
pip install -e .[build_sphinx]
python setup.py build_sphinx
```

## Usage examples

The exception class can be used as follows:

```python
from halerror import HalError

def open_pod_bay_doors():
    raise HalError("Open the pod bay doors, HAL.")

open_pod_bay_doors()
```

This will result in the following error output, where ${NAME} is the username
of the person running the software:

```
halerror.HalError: Open the pod bay doors, HAL

I'm sorry, ${NAME}. I'm afraid I can't do that.
```

Having all your exceptions formatted like this is as easy as adding the
following lines to your code

```python
from halerror import HalError

try:
    open_pod_bay_doors()
except Exception as error:
    raise HalError(error) from error
```

## Documentation

You can find the full documentation on [Read the Docs](https://halerror.readthedocs.io/en/latest).

## Issues

Please use the [GitHub issue tracker](https://github.com/jmp1985/halerror/issues) to submit bugs or request features.

## License

Copyright James Parkhurst, 2019.

Distributed under the terms of the BSD license, halerror is free and open source software.
