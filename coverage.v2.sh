#!/bin/bash
if [ -f .env.test ]; then
    export $(cat .env.test | xargs)
    docker compose -f docker-compose.dev.yml up -d
    python -m coverage run --source='api' --omit 'api/manage.py,api/config/*' api/manage.py test api/ --pattern='test*.py'
    python -m coverage report
    python -m coverage html
    docker compose -f docker-compose.dev.yml down
fi
