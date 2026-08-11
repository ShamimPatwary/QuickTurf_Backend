"""
tests/conftest.py
Shared fixtures used across all backend test modules.
Uses an in-memory SQLite database so no real Postgres is needed during testing.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_quickturf.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("SSLCOMMERZ_STORE_ID", "testbox")
os.environ.setdefault("SSLCOMMERZ_STORE_PASSWORD", "qwerty")

from app.database import Base, get_db
from app.main import app
from app.models import *  # noqa
from app.core.security import hash_password
from app.models.admin import Admin

TEST_DB_URL = "sqlite:///./test_quickturf.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestingSession()
    yield session
    session.rollback()
    session.close()


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def platform_admin_token(client, db):
    import uuid
    email = f"admin_{uuid.uuid4().hex[:6]}@quickturf.com"
    admin = Admin(name="Test Platform Admin", email=email,
                 hashed_password=hash_password("admin123"))
    db.add(admin)
    db.commit()
    resp = client.post("/api/admin/auth/login",
                       data={"username": email, "password": "admin123"})
    assert resp.status_code == 200, f"Admin login failed: {resp.text}"
    return resp.json()["access_token"]


@pytest.fixture()
def created_turf(client, platform_admin_token):
    import uuid
    email = f"turfadmin_{uuid.uuid4().hex[:6]}@test.com"
    headers = {"Authorization": f"Bearer {platform_admin_token}"}
    resp = client.post("/api/admin/turfs", json={
        "name": "Test Turf",
        "address": "123 Test Street, Dhaka",
        "phone": "+8801711111111",
        "turf_admin_email": email,
        "turf_admin_password": "turf123",
    }, headers=headers)
    assert resp.status_code == 200, f"Turf creation failed: {resp.text}"
    turf = resp.json()

    login = client.post("/api/turf-admin/auth/login",
                        data={"username": email, "password": "turf123"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"turf": turf, "token": token, "headers": {"Authorization": f"Bearer {token}"}}


@pytest.fixture()
def turf_with_sport_and_slot(client, created_turf):
    headers = created_turf["headers"]
    sport_resp = client.post("/api/turf-admin/sports",
                             json={"name": "football"}, headers=headers)
    assert sport_resp.status_code == 200
    sport = sport_resp.json()

    slot_resp = client.post("/api/turf-admin/time-slots", json={
        "sport_id": sport["id"], "start_time": "18:00:00",
        "end_time": "19:00:00", "price": 1000,
    }, headers=headers)
    assert slot_resp.status_code == 200
    slot = slot_resp.json()

    return {**created_turf, "sport": sport, "slot": slot}
