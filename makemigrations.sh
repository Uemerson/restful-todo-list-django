#!/bin/sh
export DJANGO_SECRET_KEY=$(echo $RANDOM | md5sum | head -c 30)
source .venv/bin/activate
python api/manage.py makemigrations