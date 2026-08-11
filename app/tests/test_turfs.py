"""tests/test_turfs.py — TC09-TC18: Turf CRUD, suspend/activate, sports, public browsing."""
import uuid


class TestTurfCRUD:
    def test_TC09_create_turf_with_phone(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        email = f"ta_{uuid.uuid4().hex[:6]}@test.com"
        resp = client.post("/api/admin/turfs", json={
            "name": "Phone Turf", "address": "456 Main Rd, Dhaka", "phone": "+8801800000001",
            "turf_admin_email": email, "turf_admin_password": "pass123",
        }, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Phone Turf"
        assert data["phone"] == "+8801800000001"

    def test_TC10_list_turfs(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.get("/api/admin/turfs", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_TC11_get_single_turf(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        resp = client.get(f"/api/admin/turfs/{turf_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == turf_id

    def test_TC12_update_turf(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        resp = client.put(f"/api/admin/turfs/{turf_id}",
                          json={"name": "Updated Turf Name", "phone": "+8801900000001"},
                          headers=headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Turf Name"

    def test_TC13_suspend_turf(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        resp = client.patch(f"/api/admin/turfs/{turf_id}/status",
                            json={"status": "suspended"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "suspended"

    def test_TC14_activate_turf(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        resp = client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "active"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "active"


class TestTurfAdminSports:
    def test_TC15_create_sport(self, client, created_turf):
        resp = client.post("/api/turf-admin/sports", json={"name": "cricket"}, headers=created_turf["headers"])
        assert resp.status_code == 200
        assert resp.json()["name"] == "cricket"

    def test_TC16_create_time_slot(self, client, turf_with_sport_and_slot):
        data = turf_with_sport_and_slot
        assert data["slot"]["price"] == 1000
        assert data["slot"]["start_time"] == "18:00:00"

    def test_TC17_suspended_turf_blocked_from_adding_sport(self, client, platform_admin_token, created_turf):
        admin_headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=admin_headers)
        resp = client.post("/api/turf-admin/sports", json={"name": "basketball"}, headers=created_turf["headers"])
        assert resp.status_code == 403
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "active"}, headers=admin_headers)


class TestPublicTurfs:
    def test_TC18_public_browse_active_turfs(self, client, created_turf):
        resp = client.get("/api/public/turfs")
        assert resp.status_code == 200

    def test_TC18b_public_browse_filter_by_sport(self, client, turf_with_sport_and_slot):
        resp = client.get("/api/public/turfs", params={"sport_name": "football"})
        assert resp.status_code == 200

    def test_TC18c_public_get_turf_detail(self, client, created_turf):
        turf_id = created_turf["turf"]["id"]
        resp = client.get(f"/api/public/turfs/{turf_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == turf_id
