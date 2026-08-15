"""tests/test_crud_completeness.py — TC91-TC115: Full update/delete coverage for sports, slots, packages, memberships, images."""


class TestSportUpdateDelete:
    def test_TC91_update_sport_name(self, client, created_turf):
        headers = created_turf["headers"]
        sport = client.post("/api/turf-admin/sports", json={"name": "badminton"}, headers=headers).json()
        resp = client.put(f"/api/turf-admin/sports/{sport['id']}", json={"name": "table tennis"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "table tennis"

    def test_TC92_update_nonexistent_sport_returns_404(self, client, created_turf):
        resp = client.put("/api/turf-admin/sports/999999", json={"name": "ghost"}, headers=created_turf["headers"])
        assert resp.status_code == 404

    def test_TC93_delete_sport(self, client, created_turf):
        headers = created_turf["headers"]
        sport = client.post("/api/turf-admin/sports", json={"name": "rugby"}, headers=headers).json()
        resp = client.delete(f"/api/turf-admin/sports/{sport['id']}", headers=headers)
        assert resp.status_code == 200
        names = [s["name"] for s in client.get("/api/turf-admin/sports", headers=headers).json()]
        assert "rugby" not in names

    def test_TC94_delete_nonexistent_sport_returns_404(self, client, created_turf):
        resp = client.delete("/api/turf-admin/sports/999999", headers=created_turf["headers"])
        assert resp.status_code == 404


class TestTimeSlotUpdateDelete:
    def test_TC95_update_time_slot_price(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.put(f"/api/turf-admin/time-slots/{d['slot']['id']}", json={"price": 1500}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["price"] == 1500

    def test_TC96_deactivate_time_slot(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.put(f"/api/turf-admin/time-slots/{d['slot']['id']}", json={"is_active": False}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    def test_TC97_deactivated_slot_not_shown_as_available(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.put(f"/api/turf-admin/time-slots/{d['slot']['id']}", json={"is_active": False}, headers=d["headers"])
        resp = client.get(f"/api/public/turfs/{d['turf']['id']}/sports/{d['sport']['id']}/available-slots",
                          params={"booking_date": "2027-03-01"})
        slot_ids = [s["id"] for s in resp.json()]
        assert d["slot"]["id"] not in slot_ids

    def test_TC98_delete_time_slot(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.delete(f"/api/turf-admin/time-slots/{d['slot']['id']}", headers=d["headers"])
        assert resp.status_code == 200

    def test_TC99_update_nonexistent_time_slot_returns_404(self, client, created_turf):
        resp = client.put("/api/turf-admin/time-slots/999999", json={"price": 100}, headers=created_turf["headers"])
        assert resp.status_code == 404


class TestPackageUpdateDelete:
    def test_TC100_update_package_price(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        pkg = client.post("/api/turf-admin/packages", json={
            "name": "Update Test Pack", "price": 1000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.put(f"/api/turf-admin/packages/{pkg['id']}", json={"price": 1200}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["price"] == 1200

    def test_TC101_update_package_sport_ids(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        cricket = client.post("/api/turf-admin/sports", json={"name": "cricket_update_test"}, headers=d["headers"]).json()
        pkg = client.post("/api/turf-admin/packages", json={
            "name": "Multi Sport Pack", "price": 1000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.put(f"/api/turf-admin/packages/{pkg['id']}",
                          json={"sport_ids": [d["sport"]["id"], cricket["id"]]}, headers=d["headers"])
        assert resp.status_code == 200
        assert len(resp.json()["sports"]) == 2

    def test_TC102_deactivate_package(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        pkg = client.post("/api/turf-admin/packages", json={
            "name": "Deactivate Test Pack", "price": 1000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.put(f"/api/turf-admin/packages/{pkg['id']}", json={"is_active": False}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    def test_TC103_inactive_package_hidden_from_public(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        pkg = client.post("/api/turf-admin/packages", json={
            "name": "Hidden Pack", "price": 1000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        client.put(f"/api/turf-admin/packages/{pkg['id']}", json={"is_active": False}, headers=d["headers"])
        resp = client.get(f"/api/public/turfs/{d['turf']['id']}/packages", params={"sport_id": d["sport"]["id"]})
        assert "Hidden Pack" not in [p["name"] for p in resp.json()]

    def test_TC104_delete_package(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        pkg = client.post("/api/turf-admin/packages", json={
            "name": "Delete Test Pack", "price": 1000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.delete(f"/api/turf-admin/packages/{pkg['id']}", headers=d["headers"])
        assert resp.status_code == 200


class TestMembershipUpdateDelete:
    def test_TC105_update_membership_discount(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        m = client.post("/api/turf-admin/memberships", json={
            "name": "Update Discount Test", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.put(f"/api/turf-admin/memberships/{m['id']}", json={"discount_percentage": 25}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["discount_percentage"] == 25

    def test_TC106_update_membership_duration(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        m = client.post("/api/turf-admin/memberships", json={
            "name": "Update Duration Test", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.put(f"/api/turf-admin/memberships/{m['id']}", json={"duration_days": 60}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["duration_days"] == 60

    def test_TC107_deactivate_membership(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        m = client.post("/api/turf-admin/memberships", json={
            "name": "Deactivate Membership Test", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.put(f"/api/turf-admin/memberships/{m['id']}", json={"is_active": False}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    def test_TC108_inactive_membership_hidden_from_public(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        m = client.post("/api/turf-admin/memberships", json={
            "name": "Hidden Membership", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        client.put(f"/api/turf-admin/memberships/{m['id']}", json={"is_active": False}, headers=d["headers"])
        resp = client.get(f"/api/public/turfs/{d['turf']['id']}/memberships")
        assert "Hidden Membership" not in [x["name"] for x in resp.json()]

    def test_TC109_delete_membership(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        m = client.post("/api/turf-admin/memberships", json={
            "name": "Delete Membership Test", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.delete(f"/api/turf-admin/memberships/{m['id']}", headers=d["headers"])
        assert resp.status_code == 200

    def test_TC110_update_nonexistent_membership_returns_404(self, client, turf_with_sport_and_slot):
        resp = client.put("/api/turf-admin/memberships/999999", json={"price": 1}, headers=turf_with_sport_and_slot["headers"])
        assert resp.status_code == 404


class TestTurfImageManagement:
    def test_TC111_upload_turf_image(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        resp = client.post(f"/api/admin/turfs/{turf_id}/images",
                           files={"file": ("test.jpg", b"fake-image-bytes", "image/jpeg")}, headers=headers)
        assert resp.status_code == 200
        assert "image_url" in resp.json()

    def test_TC112_uploaded_image_appears_in_turf_detail(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.post(f"/api/admin/turfs/{turf_id}/images",
                   files={"file": ("test2.jpg", b"more-fake-bytes", "image/jpeg")}, headers=headers)
        resp = client.get(f"/api/admin/turfs/{turf_id}", headers=headers)
        assert len(resp.json()["images"]) >= 1

    def test_TC113_delete_turf_image(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        img = client.post(f"/api/admin/turfs/{turf_id}/images",
                          files={"file": ("test3.jpg", b"delete-me-bytes", "image/jpeg")}, headers=headers).json()
        resp = client.delete(f"/api/admin/turfs/{turf_id}/images/{img['id']}", headers=headers)
        assert resp.status_code == 200

    def test_TC114_delete_nonexistent_image_returns_404(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        resp = client.delete(f"/api/admin/turfs/{turf_id}/images/999999", headers=headers)
        assert resp.status_code == 404

    def test_TC115_upload_image_without_file_returns_422(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        resp = client.post(f"/api/admin/turfs/{turf_id}/images", headers=headers)
        assert resp.status_code == 422
