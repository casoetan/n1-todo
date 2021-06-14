# N1 Todo

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code coverage: pytest](https://img.shields.io/badge/coverage-92-green)](https://github.com/pytest-dev/pytest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Webargs)

A simple todo application built with Python using Flask and SQLite.

## Dependencies

- [Flask](https://github.com/pallets/flask)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Marshmallow](https://github.com/marshmallow-code/marshmallow)
- [Webargs](https://github.com/marshmallow-code/webargs)

## Setup

This project uses `poetry` for managing python dependencies.

### Steps get started

- Clone repository

- Install Python Poetry

```sh
brew install poetry
```

> Following commands should be run from inside cloned directory
- Install dependencies

```sh
poetry install
```

- Setup database

```sh
flask db upgrade
```

- Start application

```sh
flask run
```

## Testing

The project uses [pytest](https://github.com/pytest-dev/pytest) for testing

```sh
pytest --cov ./todo_api
```
