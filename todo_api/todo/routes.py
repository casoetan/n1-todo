from flask_restful import Resource
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import BadRequest, NotFound

from todo_api.db import db
from todo_api.todo.models import Todo, TodoStatus
from todo_api.todo.schemas import TodoFilterSchema, TodoPatchSchema, TodoSchema

TODO_ENDPOINT = "/api/todos/<string:id>"
TODO_LIST_ENDPOINT = "/api/todos"


class TodoResource(Resource):
    """Todo API Resource

    Handles a TODO API
    """

    def get(self, id):
        """Get todos

        Retrieves a todo by id

        :param id: Todo ID to retrieve
        :return: Todo
        """
        todo = Todo.query.filter_by(id=id).join("status").first()
        todo_json = TodoSchema().dump(todo)

        if not todo_json:
            raise NotFound("No todo with this ID")

        return todo_json

    def delete(self, id):
        """Delete a todo

        :param id: Todo ID to retrieve
        """
        try:
            Todo.query.filter_by(id=id).delete()
            db.session.commit()
        except AttributeError:
            raise BadRequest("Todo does not exist")

        return None, 204

    @use_kwargs(TodoPatchSchema(partial=True), location="json")
    def patch(self, id, **kwargs):
        """Patch a todo

        Update a todo's ddue date/status/name or description

        :param id: Todo ID to update
        :return: Updated Todo
        """
        if kwargs.get("status") is not None:
            status_id = kwargs.pop("status")
            status = TodoStatus.query.filter_by(id=status_id).first()
            if not status:
                raise BadRequest("Invalid status specified")
            kwargs["status_id"] = status.id

        no_updated_records = Todo.query.filter_by(id=id).update(kwargs)
        if not no_updated_records:
            raise BadRequest("Todo does not exist")

        db.session.commit()
        todo = Todo.query.filter_by(id=id).first()
        return TodoSchema().dump(todo)


class TodoListResource(Resource):
    """Todo API Resource

    Handles a list of TODOs API
    """

    @use_args(TodoFilterSchema(), location="querystring")
    def get(self, args):
        """Get todos

        Retrieves all todos (filterable) when no id is provided

        :return: Todos
        """
        return self._get_todos(**args)

    def _get_todos(self, **kwargs):
        todos = Todo.query
        if kwargs["status"]:
            todos = todos.filter_by(**{"status_id": kwargs["status"]})
        if kwargs["due_soon"]:
            todos = todos.order_by("due_date")
        else:
            todos = todos.order_by("created_at")

        todos = todos.all()

        return TodoSchema().dump(todos, many=True)

    @use_args(TodoSchema(), location="json")
    def post(self, todo):
        """Create new todos

        Create a todo

        :return: Created todo
        """
        db.session.add(todo)
        db.session.commit()

        return TodoSchema().dump(todo), 201
