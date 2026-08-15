"""tests/test_auth.py — TC01-TC08: Platform admin & turf admin authentication."""
import uuid
from app.core.security import hash_password
from app.models.admin import Admin


class TestPlatformAdminAuth:
    def test_TC01_login_success(self, client, db):
        email = f"admin_{uuid.uuid4().hex[:6]}@qt.com"
        admin = Admin(name="Admin", email=email, hashed_password=hash_password("admin123"))
        db.add(admin); db.commit()
        resp = client.post("/api/admin/auth/login", data={"username": email, "password": "admin123"})
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["role"] == "platform_admin"

    def test_TC02_login_wrong_password(self, client, db):
        email = f"admin_{uuid.uuid4().hex[:6]}@qt.com"
        admin = Admin(name="Admin", email=email, hashed_password=hash_password("correctpass"))
        db.add(admin); db.commit()
        resp = client.post("/api/admin/auth/login", data={"username": email, "password": "wrongpass"})
        assert resp.status_code == 401

    def test_TC03_access_protected_route_without_token(self, client):
        resp = client.get("/api/admin/turfs")
        assert resp.status_code == 401

    def test_TC04_access_protected_route_with_invalid_token(self, client):
        resp = client.get("/api/admin/turfs", headers={"Authorization": "Bearer fake.token.here"})
        assert resp.status_code == 401


class TestTurfAdminAuth:
    def test_TC05_turf_admin_login_success(self, client, created_turf):
        assert created_turf["token"] is not None
        assert len(created_turf["token"]) > 10

    def test_TC06_turf_admin_wrong_password(self, client, created_turf):
        resp = client.post("/api/turf-admin/auth/login",
                           data={"username": "wrong@email.com", "password": "wrongpass"})
        assert resp.status_code == 401

    def test_TC07_change_password_success(self, client, created_turf):
        resp = client.post("/api/turf-admin/auth/change-password",
                           json={"old_password": "turf123", "new_password": "newpass456"},
                           headers=created_turf["headers"])
        assert resp.status_code == 200
        assert "successfully" in resp.json()["detail"].lower()

    def test_TC08_change_password_wrong_old(self, client, created_turf):
        resp = client.post("/api/turf-admin/auth/change-password",
                           json={"old_password": "completelyWrong", "new_password": "newpass456"},
                           headers=created_turf["headers"])
        assert resp.status_code == 400
