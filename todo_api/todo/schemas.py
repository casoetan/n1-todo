from marshmallow import Schema, fields, post_load

from todo_api.todo.models import Todo


class TodoStatusSchema(Schema):
    """TodoStatus Marshmallow Schema

    Schema used for loading and dumping Todo Statuses
    """

    id = fields.Integer()
    label = fields.String(allow_none=False)


class TodoSchema(Schema):
    """Todo Marshmallow Schema

    Schema used for loading and dumping Todo
    """

    id = fields.UUID()
    title = fields.String(allow_none=False)
    description = fields.String()
    due_date = fields.Date()
    status_id = fields.Integer(load_only=True)
    created_at = fields.Date(dump_only=True)
    updated_at = fields.Date(dump_only=True)
    status = fields.Nested(TodoStatusSchema(only={"id", "label"}), dump_only=True)

    @post_load
    def make_todo(self, data, **kwargs):
        return Todo(**data)


class TodoPatchSchema(Schema):
    """Todo patch Marshmallow Schema

    Schema for patching todos
    """

    title = fields.String()
    due_date = fields.Date()
    status = fields.Integer()


class TodoFilterSchema(Schema):
    """Todo filter Marshmallow Schema

    Schema for filtering/sorting todos by status and due date
    """
    due_soon = fields.Boolean(missing=True)
    status = fields.Integer(missing=1)
