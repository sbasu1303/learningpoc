#!/bin/bash
PY_DIR=`which python3.8`
echo $DS_ENV
if [ -z "$DS_ENV" ]; then
  export DS_ENV='DEV'
fi
if [ "$DS_ENV" == "LOCAL" ]; then
  export PROJ_PATH=`pwd`
  export BASE_LOG_DIR=`pwd`'/logs'
else
  export PROJ_PATH='/usr/src/app'
  export BASE_LOG_DIR='/var/logs'
fi

$PY_DIR $PROJ_PATH/manage.py clearsessions