import uuid

from flask_sqlalchemy import SQLAlchemy

"""Database configurations

Configure an SQLite database
"""
db = SQLAlchemy()


def generate_uuid():
    return uuid.uuid4().hex
