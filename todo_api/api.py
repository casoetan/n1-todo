import logging

from flask import Flask
from flask_restful import Api

from todo_api.constants import PROJECT_ROOT, TODO_DATABASE
from todo_api.db import db
from todo_api.todo.routes import (
    TODO_ENDPOINT,
    TODO_LIST_ENDPOINT,
    TodoListResource,
    TodoResource,
)


def create_app():
    """Creates Flask application.

    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection

    :param db_location: Connection string to the database
    :test_config: Configuration for testing
    :return: Initialized Flask app
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("todo_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{PROJECT_ROOT}/{TODO_DATABASE}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    @app.before_first_request
    def load_initial_data():
        from todo_api import load_data

        load_data.load_fixtures()

    api = Api(app)
    api.add_resource(TodoResource, TODO_ENDPOINT)
    api.add_resource(TodoListResource, TODO_LIST_ENDPOINT)

    return app
