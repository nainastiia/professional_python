import pytest
from httpx import AsyncClient, ASGITransport
from warehouse_system.api import app, repo


@pytest.fixture(autouse=True)
def clear_repository():
    repo.clear()


@pytest.mark.asyncio
async def test_create_and_read_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/items",
            json={"code": "T1", "name": "Test Item", "quantity": 5, "price": 50.0}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "T1"

        get_res = await client.get("/items/T1")
        assert get_res.status_code == 200
        assert get_res.json()["name"] == "Test Item"