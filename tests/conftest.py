import json
from pathlib import Path

import pytest

from todo_api.api import create_app
from todo_api.db import db
from todo_api.todo.schemas import TodoSchema


@pytest.fixture(scope="module")
def app():
    db_path = f"{Path(__file__).parent}/n1_todo_test.db"
    app = create_app(db_path)
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.init_app(app)
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def load_data(app):
    with open(f"{Path(__file__).parent}/fixtures.json") as fixture_file:
        fixtures_data = json.load(fixture_file)

    with app.app_context():
        for todo_obj in fixtures_data:
            todo = TodoSchema(context={"raw": True}).load(todo_obj)
            db.session.add(todo)

        db.session.commit()


@pytest.fixture(scope="module")
def client(app, load_data):
    with app.test_client() as client:
        yield client
