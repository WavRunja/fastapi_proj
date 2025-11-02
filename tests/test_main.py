# tests/test_main.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import Base, engine

# Создаём чистую БД перед каждым тестом


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_create_and_read_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Создаём пользователя
        response = await client.post(
            "/users/",
            params={"name": "Apps_User_0", "email": "Apps_User_0@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Apps_User_0"
        assert data["email"] == "Apps_User_0@example.com"

        # 2. Проверяем, что пользователь сохранился
        response = await client.get("/users/")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 1
        assert users[0]["id"] == 1
        assert users[0]["name"] == "Apps_User_0"
        assert users[0]["email"] == "Apps_User_0@example.com"
