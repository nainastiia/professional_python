from fastapi.testclient import TestClient
import pytest
from warehouse_system.api import app
from warehouse_system.database import get_session


@pytest.fixture
def client(db_session):
    def override_get_session():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_and_get_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Keyboard",
            "sku": "KB-100",
            "price": 45.0,
            "quantity": 10,
            "min_stock_level": 3,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Keyboard"
    product_id = data["id"]

    get_res = client.get(f"/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["sku"] == "KB-100"


def test_write_off_exceeds_stock(client):
    create_res = client.post(
        "/products",
        json={
            "name": "Monitor",
            "sku": "MN-500",
            "price": 200.0,
            "quantity": 2,
            "min_stock_level": 1,
        },
    )
    product_id = create_res.json()["id"]

    write_off_res = client.post(
        f"/products/{product_id}/write-off", json={"amount": 5}
    )
    assert write_off_res.status_code == 400
    assert "exceeds" in write_off_res.json()["detail"].lower()


def test_validation_error(client):
    response = client.post(
        "/products",
        json={
            "name": "X",
            "sku": "ERR",
            "price": -10.0,
            "quantity": -1,
        },
    )
    assert response.status_code == 422