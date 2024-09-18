# ft_requests

A simplified 'requests' clone, built with http.client from Python's standard library, allowing easy migration by replacing requests with ft_requests.

# Installation

pip install <.whl file>

If you encounter an error like:
```py
TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'

```
Execute this command:
```sh
pip install packaging==22.0
```
See discussions here: https://github.com/pypa/setuptools/issues/4501
