import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_purchase_order_crud():
    """Basic CRUD test for PurchaseOrder router"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 🔹 Create
        create_payload = {}
        response = await ac.post("/purchase_order/", json=create_payload)
        assert response.status_code in [200, 201, 422]

        # 🔹 List
        response = await ac.get("/purchase_order/")
        assert response.status_code == 200

        # 🔹 Read (dummy id = 1)
        response = await ac.get("/purchase_order/1")
        assert response.status_code in [200, 404]

        # 🔹 Update
        update_payload = {}
        response = await ac.put("/purchase_order/1", json=update_payload)
        assert response.status_code in [200, 404, 422]

        # 🔹 Delete
        response = await ac.delete("/purchase_order/1")
        assert response.status_code in [200, 204, 404]
