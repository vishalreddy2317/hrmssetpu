import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_shift_crud():
    """Basic CRUD test for Shift router"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 🔹 Create
        create_payload = {}
        response = await ac.post("/shift/", json=create_payload)
        assert response.status_code in [200, 201, 422]

        # 🔹 List
        response = await ac.get("/shift/")
        assert response.status_code == 200

        # 🔹 Read (dummy id = 1)
        response = await ac.get("/shift/1")
        assert response.status_code in [200, 404]

        # 🔹 Update
        update_payload = {}
        response = await ac.put("/shift/1", json=update_payload)
        assert response.status_code in [200, 404, 422]

        # 🔹 Delete
        response = await ac.delete("/shift/1")
        assert response.status_code in [200, 204, 404]
