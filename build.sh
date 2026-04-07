# clean previous builds
rm -rf dist/

# build wheel only (no source distribution)
python -m build --wheel

# upload only the wheel to testpypi
twine upload --repository testpypi dist/*.whl

