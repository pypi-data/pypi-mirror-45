# bunnieddpg

This is a Python library that contains a Deep Deterministic Policy Gradients autonomous agent.

## Upload Python package to PyPI

To upload the Python package, you need to install `twine`:

```shell
$ pip install twine
```

Next, upload the Python package to PyPI:

```shell
# Copy from: https://pypi.org/project/twine/
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```
