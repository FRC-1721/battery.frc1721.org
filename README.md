=== battery.frc1721.org ===

https://battery.frc1721.org/

Django server to keep track of the state of batteries.
Made by dublu.

----- TODO

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
