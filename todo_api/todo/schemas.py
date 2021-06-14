import json
from datetime import date

from marshmallow import Schema, fields, post_dump, post_load, pre_load
from marshmallow.decorators import validates_schema
from marshmallow.exceptions import ValidationError

from todo_api.todo.models import Todo


def due_date_in_future(data):
    if not data:
        pass

    if data < date.today():
        raise ValidationError("Due date cannot be in the past")


class TodoStatusSchema(Schema):
    """TodoStatus Marshmallow Schema

    Schema used for loading and dumping Todo Statuses
    """

    id = fields.Integer()
    label = fields.String(allow_none=False)


class TodoSchema(Schema):
    """Todo Marshmallow Schema

    Schema for loading and dumping Todos
    """

    id = fields.String()
    title = fields.String(
        allow_none=False,
        required=True,
    )
    description = fields.String()
    due_date = fields.Date()
    tags = fields.String()
    status_id = fields.Integer(load_only=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    status = fields.Nested(TodoStatusSchema(only={"id", "label"}), dump_only=True)

    @pre_load
    def parse_todo_tags(self, data, **kwargs):
        tags = data.get("tags", [])
        if type(tags) != list:
            raise ValidationError("Invalid tags")
        data["tags"] = json.dumps(tags)
        return data

    @post_load
    def make_todo(self, data, **kwargs):
        return Todo(**data)

    @post_dump
    def process_todo_tags(self, data, **kwargs):
        if not data:
            return
        data["tags"] = json.loads(data["tags"])
        return data

    @validates_schema
    def validate_date(self, data, **kwargs):
        if (
            self.context.get("raw") is False
            and data.get("due_date")
            and data["due_date"] < date.today()
        ):
            raise ValidationError("Due date cannot be in the past")


class TodoPatchSchema(Schema):
    """Todo patch Marshmallow Schema

    Schema for patching todos
    """

    title = fields.String()
    due_date = fields.Date(validate=due_date_in_future)
    status = fields.Integer()


class TodoFilterSchema(Schema):
    """Todo filter Marshmallow Schema

    Schema for filtering/sorting todos by status and due date
    """

    past_due = fields.Boolean(missing=False)
    due_soon = fields.Boolean(missing=True)
    status = fields.Integer(missing=1)
