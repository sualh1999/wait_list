import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.config import settings # Import settings to access ADMIN_PASSWORD
from backend.app.utils.geo import get_country_from_ip

# Setup a test database
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(autouse=True)
def mock_geo_ip(monkeypatch):
    async_mock = AsyncMock(return_value="Testland")
    monkeypatch.setattr(get_country_from_ip, "__wrapped__", async_mock)

@pytest.fixture(name="db_session")
async def db_session_fixture():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(name="client")
async def client_fixture(db_session: AsyncSession):
    def override_get_db():
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_waitlist_entry(client: AsyncClient):
    response = await client.post("/waitlist", json={
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["country"] == "Testland"

@pytest.mark.asyncio
async def test_create_waitlist_entry_duplicate_email(client: AsyncClient):
    response = await client.post("/waitlist", json={
        "email": "duplicate@example.com",
        "first_name": "Jane",
        "last_name": "Doe"
    })
    assert response.status_code == 201

    response = await client.post("/waitlist", json={
        "email": "duplicate@example.com",
        "first_name": "Jane",
        "last_name": "Doe"
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already on waitlist"

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_admin_login_success(client: AsyncClient):
    response = await client.post("/admin/login", json={"password": settings.ADMIN_PASSWORD})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_admin_login_failure(client: AsyncClient):
    response = await client.post("/admin/login", json={"password": "wrong_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"

@pytest.mark.asyncio
async def test_admin_list_unauthorized(client: AsyncClient):
    response = await client.get("/admin/list")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_admin_list_authorized(client: AsyncClient):
    # First, log in to get a token
    login_response = await client.post("/admin/login", json={"password": settings.ADMIN_PASSWORD})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Add some waitlist entries
    await client.post("/waitlist", json={
        "email": "admin1@example.com",
        "first_name": "Admin",
        "last_name": "One"
    })
    await client.post("/waitlist", json={
        "email": "admin2@example.com",
        "first_name": "Admin",
        "last_name": "Two"
    })

    # Then, request the list with the token
    list_response = await client.get("/admin/list", headers={"Authorization": f"Bearer {token}"})
    assert list_response.status_code == 200
    entries = list_response.json()
    assert len(entries) >= 2 # May include entries from other tests if db not fully reset
    assert any(entry["email"] == "admin1@example.com" and entry["first_name"] == "Admin" and entry["last_name"] == "One" and entry["country"] == "Testland" for entry in entries)
    assert any(entry["email"] == "admin2@example.com" and entry["first_name"] == "Admin" and entry["last_name"] == "Two" and entry["country"] == "Testland" for entry in entries)
