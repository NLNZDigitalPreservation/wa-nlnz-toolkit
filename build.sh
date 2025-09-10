# build python package
python -m build

# upload the package to testpypi
twine upload --repository testpypi dist/*

