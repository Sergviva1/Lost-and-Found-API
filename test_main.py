from fastapi.testclient import TestClient
from main import app, items

client = TestClient(app)


def test_get_first_item():
    items.clear()

    client.post("/items", json={"title": "Телефон", "category": "Электроника"})

    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_second_item():
    items.clear()

    client.post("/items", json={"title": "Телефон", "category": "Электроника"})
    client.post("/items", json={"title": "Холодильник", "category": "Бытовая техника"})

    response = client.get("/items/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2
    assert response.json()["title"] == "Холодильник"


def test_get_nonexistent_item():
    items.clear()

    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_create_item_empty_file():
    items.clear()

    response = client.post("/items", json={"title": "", "category": "Электроника"})

    assert response.status_code == 422
    assert len(items) == 0
