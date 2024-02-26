#!/bin/bash
# docker exec -it todolist_api sh -c "cd api/ && python manage.py test --pattern='test*.py'"
docker compose -f docker-compose.dev.yml run api sh -c "cd api/ && python manage.py test --pattern='test*.py'"
docker compose -f docker-compose.dev.yml down
