#!/bin/bash

NAME="worker"                                 # Name of the application
DJANGODIR=/home/manto/sensait/sensait_django      # Django project directory
USER=manto                                        # the user to run as
GROUP=manto                                       # the group to run as
DJANGO_SETTINGS_MODULE=ardsensor.settings         # which settings file should Django use

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/manto/.venvs/sensait_channels/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec python manage.py runworker