#!/bin/sh

# pip install --upgrade build
# pip install --upgrade twine

rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q qgate_sln_mlrun.egg-info

# helper 'https://www.scivision.dev/python-minimal-package/'
# https://pypa-build.readthedocs.io/en/latest/
python -m build --wheel

# twine upload is supported
twine upload dist/* --verbose -u__token__

rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q qgate_sln_mlrun.egg-info
