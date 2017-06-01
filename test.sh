#!/bin/bash

set -e

cd $(dirname $0)

pipenv run python setup.py sdist
pipenv run python setup.py flake8
pipenv run pytest subdlsrv
