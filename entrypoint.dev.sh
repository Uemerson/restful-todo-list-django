#!/bin/sh
python api/manage.py migrate
exec "$@"