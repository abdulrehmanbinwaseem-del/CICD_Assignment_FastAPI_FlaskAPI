from fastapi.testclient import TestClient
from main import app, tasks

client = TestClient(app)


def setup_function():
    """Reset shared in-memory task list before each test so tests stay
    independent of execution order."""
    tasks.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["done"] is False


def test_get_tasks_grows():
    initial = client.get("/tasks").json()
    assert isinstance(initial, list)
    assert len(initial) == 0

    client.post("/tasks", json={"title": "Buy milk"})
    after = client.get("/tasks").json()

    assert isinstance(after, list)
    assert len(after) == len(initial) + 1
    assert any(task["title"] == "Buy milk" for task in after)


def test_create_task_empty_title_fails():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
    assert "Title cannot be empty" in response.json()["detail"]


def test_create_task_missing_title_fails():
    response = client.post("/tasks", json={"done": True})
    assert response.status_code == 422
