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
mkdir -p "$BASE_LOG_DIR""/ds_django"
mkdir -p "$BASE_LOG_DIR""/uwsgi"
ps -ef | grep celery | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep uwsgi | grep -v grep | awk '{print $2}'|xargs kill -9
$PY_DIR $PROJ_PATH/manage.py migrate
#

$PY_DIR $PROJ_PATH/manage.py collectstatic --noinput
$PY_DIR $PROJ_PATH/manage.py clearsessions

export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin:/etc
systemctl enable cron
(crontab -l 2>/dev/null; echo "*/5 * * * * " $PROJ_PATH/session_clean.sh) | crontab -

$PROJ_PATH/celery_beat.sh &
$PROJ_PATH/celery_worker.sh &
uwsgi --static-map /static=$PROJ_PATH/static --ini $PROJ_PATH/uwsgi.ini #--daemonize "$BASE_LOG_DIR""/uwsgi/uwsgi.log"