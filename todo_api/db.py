import uuid

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

"""Database configurations

Configure an SQLite database
"""
db = SQLAlchemy()
migrate = Migrate()


def generate_uuid():
    return uuid.uuid4().hex
