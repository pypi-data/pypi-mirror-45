# Machine Learning - Python utility functions

Convenient Python utility functions commonly used in the AI machine learning 
projects.

## Build Package

References:
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi)

Dependencies: `setuptools`, `wheel` and `twine`

```
$ python setup.py sdist bdist_wheel

# For testing, upload to test.pypi.org
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Install package from test.pypi.org
pip install --index-url https://test.pypi.org/simple/ --no-deps mlfns

# Release upload to pypi.org
$ twine upload --repository-url https://pypi.org/legacy/ dist/*

# Install package from test.pypi.org
pip install --index-url https://pypi.org/simple/ --no-deps mlfns
```