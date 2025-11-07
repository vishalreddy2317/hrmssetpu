import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_payment_crud():
    """Basic CRUD test for Payment router"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 🔹 Create
        create_payload = {}
        response = await ac.post("/payment/", json=create_payload)
        assert response.status_code in [200, 201, 422]

        # 🔹 List
        response = await ac.get("/payment/")
        assert response.status_code == 200

        # 🔹 Read (dummy id = 1)
        response = await ac.get("/payment/1")
        assert response.status_code in [200, 404]

        # 🔹 Update
        update_payload = {}
        response = await ac.put("/payment/1", json=update_payload)
        assert response.status_code in [200, 404, 422]

        # 🔹 Delete
        response = await ac.delete("/payment/1")
        assert response.status_code in [200, 204, 404]
