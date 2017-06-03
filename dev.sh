#!/bin/bash

set -e

cd $(dirname $0)
basedir=$1
shift

if [[ ! -z $basedir ]]; then
    basedir_arg="--basedir $basedir --mapping tv=Series"
else
    basedir_arg=""
fi

PORT=8086

echo "Starting subdlrv on port $PORT:"
export SUBDLSRC_LANGUAGES="fra,eng"
pipenv run subdlsrv --port $PORT --verbose $basedir_arg
