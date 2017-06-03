#!/bin/bash

set -e

cd $(dirname $0)

echo "Test local build"
pipenv run python setup.py sdist
pipenv run python setup.py flake8
echo "Running pylint"
pipenv run pylint --rcfile=setup.cfg subdlsrv
pipenv run pytest subdlsrv
