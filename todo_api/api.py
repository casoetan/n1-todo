import json
import logging

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from todo_api.constants import PROJECT_ROOT, TODO_DATABASE
from todo_api.db import db, migrate
from todo_api.todo.resources import (
    TODO_ENDPOINT,
    TODO_LIST_ENDPOINT,
    TodoListResource,
    TodoResource,
)


def create_app(db_path=None):
    """Creates Flask application.

    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection

    :param db_location: Connection string to the database
    :db_path: Optionally specify database path
    :return: Initialized Flask app
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("todo_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)
    CORS(app)

    if db_path:
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{db_path}"
    else:
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"sqlite:////{PROJECT_ROOT}/{TODO_DATABASE}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # Setup SQLite database on first request
    @app.before_first_request
    def create_table():
        db.create_all()

    # Populate todo status table with initial data
    @app.before_first_request
    def load_initial_data():
        from todo_api import load_data

        load_data.load_fixtures()

    # Error handling
    @app.errorhandler(422)
    def handle_unprocessable_entity(e):
        response = e.get_response()

        exc = getattr(e, "exc")
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": exc.messages if exc else ["Invalid request"],
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""

        # Log exceptions
        logging.exception(e)

        # Use correct headers and status code from the error
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    # API Resources
    api = Api(app)
    api.add_resource(TodoResource, TODO_ENDPOINT)
    api.add_resource(TodoListResource, TODO_LIST_ENDPOINT)

    return app
