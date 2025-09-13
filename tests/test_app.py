import json
import pytest

from server import app

@pytest.fixture
def client():
    return app.test_client()

def test_add_new_product(client):
    payload = {"name": "oreos", "quantity": 10}
    response = client.post("/inventory", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert "oreo" in data["name"].lower()
    assert data["quantity"] == payload["quantity"]
    assert "id" in data

def test_add_incomplete_product(client):
    payload = {"name": "oreos"}
    response = client.post("/inventory", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400

def test_list_products(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()[0]
    assert isinstance(data, dict)
    assert "name" in data
    assert "oreo" in data["name"].lower()

def test_get_product(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "name" in data
    assert "oreo" in data["name"].lower()

def test_get_incorrect_product(client):
    response = client.get("/inventory/10")
    assert response.status_code == 404

def test_update_product_name(client):
    payload = {"name": "cookie"}
    response = client.patch("/inventory/1", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "cookie" in data["name"].lower()

def test_update_product_quantity(client):
    payload = {"quantity": 30}
    response = client.patch("/inventory/1", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["quantity"] == 30

def test_update_incorrect_product(client):
    payload = {"name": "cookie"}
    response = client.patch("/inventory/10", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 404

def test_delete_product(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 204

def test_delete_incorrect_product(client):
    response = client.delete("/inventory/10")
    assert response.status_code == 404