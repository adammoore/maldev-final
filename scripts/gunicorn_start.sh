#!/bin/bash

NAME="research_data_lifecycle"
DIR=/path/to/your/project
USER=your_user
GROUP=your_group
WORKERS=3
BIND=unix:/path/to/your/project/gunicorn.sock
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_WSGI_MODULE=run:app
LOG_LEVEL=error

cd $DIR
source venv/bin/activate

exec gunicorn ${DJANGO_WSGI_MODULE} \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
