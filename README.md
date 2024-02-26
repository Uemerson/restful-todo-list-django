# About

API RESTful To-Do List

# Bash scripts

- The script [up.dev.v2.sh](./up.dev.v2.sh) contains bash instructions to bring up the application using `Docker v2` and stop the containers by pressing Ctrl+C.

- The script [test.v2.sh](./test.v2.sh) contains bash instructions to run unit tests and integration tests.

- The script [coverage.v2.sh](./coverage.v2.sh) contains bash instructions to run to run code coverage.

# Instructions

This project uses [Docker and Docker Compose, so it's necessary to install them.](https://docs.docker.com/compose/install/)

After installation, rename the files `.env.dev.example` to `.env.dev` and `.env.test.example` to `.env.test`. Both are files containing environment variables with default values.

- `.env.dev`: It's used to set the environment variables used by the application.
- `.env.test`: It's used to set the environment variables used to run the [coverage bash script](./coverage.v2.sh).

Afterwards, you can bring up the containers using the bash script below:

```
$ bash up.dev.v2.sh
```

or if you don't want to use the bash script:

```
$ docker compose -f docker-compose.dev.yml --env-file .env.dev up -d --build --remove-orphans
```


## API Documentation

After bringing up the application, you can access the documentation via the following link [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

# Tests

The tests were conducted using the python standard library module `unittest` and `django test framework`. Therefore, the tests require the 'up' database. The bash script [test.v2.sh](./test.v2.sh) already brings up the application containers and runs the tests on top of it. You can run tests using the commands below:

```
$ bash test.v2.sh
```

or if you don't want to use the bash script:

```
$ docker compose -f docker-compose.dev.yml run api sh -c "cd api/ && python manage.py test --pattern='test*.py'"
```

# Coverage

**This project has 100% code coverage** (excluding the 'manage.py' file and the folder containing the project configurations)

To execute code coverage, it's recommended to have an [virtual environments](https://docs.python.org/dev/library/venv.html) and install both project dependencies from the `requirements.txt` file and development dependencies from the `requirements-dev.txt` (including coverage). You can do this using the commands below:

```
(.venv) $ pip install -r requirements.txt
```

and 

```
(.venv) $ pip install -r requirements_dev.txt
```

Afterwards, you can covarage using the bash script below:

```
(.venv) $ bash coverage.v2.sh
```

or if you don't want to use the bash script:
```
(.venv) $ export $(cat .env.test | xargs)
(.venv) $ docker compose -f docker-compose.dev.yml up -d
(.venv) $ python -m coverage run --source='api' --omit 'api/manage.py,api/config/*' api/manage.py test api/ --pattern='test*.py'
(.venv) $ python -m coverage report
(.venv) $ python -m coverage html
```

# Note

If you are using **Docker version 1 and Docker Compose version 1**, please replace `docker compose` with `docker-compose` in the bash scripts.

