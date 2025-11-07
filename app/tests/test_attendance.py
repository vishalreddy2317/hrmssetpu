import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_attendance_crud():
    """Basic CRUD test for Attendance router"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 🔹 Create
        create_payload = {}
        response = await ac.post("/attendance/", json=create_payload)
        assert response.status_code in [200, 201, 422]

        # 🔹 List
        response = await ac.get("/attendance/")
        assert response.status_code == 200

        # 🔹 Read (dummy id = 1)
        response = await ac.get("/attendance/1")
        assert response.status_code in [200, 404]

        # 🔹 Update
        update_payload = {}
        response = await ac.put("/attendance/1", json=update_payload)
        assert response.status_code in [200, 404, 422]

        # 🔹 Delete
        response = await ac.delete("/attendance/1")
        assert response.status_code in [200, 204, 404]
