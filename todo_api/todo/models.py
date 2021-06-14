# type: ignore
from datetime import datetime

from todo_api.db import db, generate_uuid


class TodoStatus(db.Model):
    """Todo Status SQLAlchemy Model

    Represents all possible todo status
    """

    __tablename__ = "todo_statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(48), nullable=False, unique=True)
    complete = db.Column(db.Boolean, default=False)


class Todo(db.Model):
    """Todo SQLAlchemy Model

    Represents objects in the todo table
    """

    __tablename__ = "todos"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    due_date = db.Column(db.Date)
    tags = db.Column(db.String(240), default="[]")
    status_id = db.Column(
        db.Integer, db.ForeignKey("todo_statuses.id"), nullable=False, default=1
    )
    status = db.relationship("TodoStatus", backref=db.backref("status"))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Todo {self.id} | {self.title} />"
