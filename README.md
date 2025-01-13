[![Build GHCR](https://github.com/FRC-1721/battery.frc1721.org/actions/workflows/build_ghcr.yml/badge.svg)](https://github.com/FRC-1721/battery.frc1721.org/actions/workflows/build_ghcr.yml)

# battery.frc1721.org

https://battery.frc1721.org/

Django server to keep track of the state of batteries.
Made by dublu.

### TODO

Sort and filter
Make it look better

## Development (using pipenv)

Use `pipenv` to manage python deps and versions

```shell
pipenv install
pipenv shell
```

Spawn a development django server

```shell
python manage.py migrate
python manage.py runserver

# Optional, do once
python3 manage.py createsuperuser
```

## Development (using docker)

In one terminal, start the `dev` requirements.

```shell
make dev
```

In another terminal, build and run a local copy of the server

```shell
make run
```

Alternatively, run the local django with the docker url string

```shell
export DATABASE_URL=postgres://battery_user:battery_password@172.18.0.2:5432/battery_db
python manage.py migrate
python manage.py runserver
```
