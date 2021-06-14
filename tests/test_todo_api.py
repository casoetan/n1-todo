from datetime import date, datetime

from todo_api.todo.resources import TODO_LIST_ENDPOINT

NUM_ACTIVE_TODOS_IN_BASE_DB = 6


def test_create_todos(client):
    new_todo_json = {"title": "Test title 1", "due_date": "2020-01-01"}
    response = client.post(f"{TODO_LIST_ENDPOINT}", json=new_todo_json)
    assert response.status_code == 201
    assert response.json["id"] is not None
    assert response.json["title"] == "Test title 1"
    assert response.json["status"] == {"label": "pending", "id": 1}


def test_create_todos_with_tags(client):
    new_todo_json = {"title": "Test tags", "tags": ["a", "b", "c"]}
    response = client.post(f"{TODO_LIST_ENDPOINT}", json=new_todo_json)
    assert response.status_code == 201
    assert len(response.json["tags"]) == 3
    assert response.json["tags"] == ["a", "b", "c"]


def test_create_todos_with_invalid_tags(client):
    new_todo_json = {"title": "Test tags", "tags": "abc"}
    response = client.post(f"{TODO_LIST_ENDPOINT}", json=new_todo_json)
    assert response.status_code == 422


def test_todos_post_error(client):
    missing_title_json = {"description": "A todo without a title"}
    response = client.post(f"{TODO_LIST_ENDPOINT}", json=missing_title_json)
    assert response.status_code == 422


def test_get_all_todos(client):
    response = client.get(f"{TODO_LIST_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == NUM_ACTIVE_TODOS_IN_BASE_DB


def test_get_all_complete_todos(client):
    response = client.get(f"{TODO_LIST_ENDPOINT}?status=2")

    for todo in response.json:
        assert todo["status"]["id"] == 2


def test_get_todos_past_due_date(client):
    response = client.get(f"{TODO_LIST_ENDPOINT}?past_due=true")

    for todo in response.json:
        assert datetime.fromisoformat(todo["due_date"]).date() < date.today()


def test_get_single_todo(client):
    response = client.get(f"{TODO_LIST_ENDPOINT}/00000000000000000000000000000001")

    assert response.status_code == 200
    assert response.json["title"] == "Todo 1"


def test_get_single_todo_not_found(client):
    response = client.get(f"{TODO_LIST_ENDPOINT}/000000000000000000000000000000A1")
    assert response.status_code == 404
