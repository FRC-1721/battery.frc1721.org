[![Build GHCR](https://github.com/FRC-1721/battery.frc1721.org/actions/workflows/build_ghcr.yml/badge.svg)](https://github.com/FRC-1721/battery.frc1721.org/actions/workflows/build_ghcr.yml)

# battery.frc1721.org

https://battery.frc1721.org/

Django server to keep track of the state of batteries.
Made by [@dublUayaychtee ](https://github.com/dublUayaychtee), [@kenwoodfox ](https://github.com/kenwoodfox).

# Development

## Development (using pipenv)

Use `pipenv` to manage python deps and versions

```shell
pipenv install
pipenv shell
```

It can be handy to place a `.env` at the root of this repo for connection details

```
DATABASE_URL=postgres://battery_user:battery_password@172.18.0.2:5432/battery_db
DEBUG=true
SECRET_KEY="fortestingonly"
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

# Maintainence tasks

There are a few custom maintenance tasks outlined in `log/management/commands`.

## addretrobattery

Useful command will walk you though adding a system-generated record to retroactively include
an older battery.

```shell
# Local
pipenv run python manage.py addretrobattery

# On prod
docker exec -it <id> ./manage.py addretrobattery
```