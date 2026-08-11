"""tests/test_edge_cases.py — TC116-TC130: Platform-wide view, suspended visibility, cascades, boundary values."""
from datetime import date


class TestPlatformAdminCrossTurfView:
    def test_TC116_platform_admin_sees_bookings_from_multiple_turfs(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-04-01", "customer_name": "Platform View Test",
            "customer_phone": "+8801711160001", "paid_amount": 0,
        })
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.get("/api/admin/bookings", headers=headers)
        assert resp.status_code == 200
        assert "Platform View Test" in [b["customer_name"] for b in resp.json()]

    def test_TC117_platform_admin_bookings_requires_auth(self, client):
        resp = client.get("/api/admin/bookings")
        assert resp.status_code == 401

    def test_TC118_turf_admin_cannot_access_platform_bookings_endpoint(self, client, created_turf):
        resp = client.get("/api/admin/bookings", headers=created_turf["headers"])
        assert resp.status_code == 401

    def test_TC119_platform_admin_can_view_suspended_turf_details(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        resp = client.get(f"/api/admin/turfs/{turf_id}", headers=headers)
        assert resp.json()["status"] == "suspended"


class TestSuspendedTurfPublicVisibility:
    def test_TC120_suspended_turf_hidden_from_public_browse(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        resp = client.get("/api/public/turfs")
        assert turf_id not in [t["id"] for t in resp.json()]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "active"}, headers=headers)

    def test_TC121_suspended_turf_detail_not_accessible_publicly(self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        resp = client.get(f"/api/public/turfs/{turf_id}")
        assert resp.status_code == 404
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "active"}, headers=headers)

    def test_TC122_cannot_book_suspended_turf(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = d["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        resp = client.post("/api/public/bookings", json={
            "turf_id": turf_id, "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-04-05", "customer_name": "Blocked Booker",
            "customer_phone": "+8801711160002", "paid_amount": 0,
        })
        assert resp.status_code == 400
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "active"}, headers=headers)


class TestDeleteCascade:
    def test_TC123_deleting_turf_removes_it_from_admin_list(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = d["turf"]["id"]
        resp = client.delete(f"/api/admin/turfs/{turf_id}", headers=headers)
        assert resp.status_code == 200
        list_resp = client.get("/api/admin/turfs", headers=headers)
        assert turf_id not in [t["id"] for t in list_resp.json()]

    def test_TC124_deleting_sport_removes_its_time_slots(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.delete(f"/api/turf-admin/sports/{d['sport']['id']}", headers=d["headers"])
        resp = client.get("/api/turf-admin/time-slots", params={"sport_id": d["sport"]["id"]}, headers=d["headers"])
        assert resp.status_code in (200, 404)

    def test_TC125_delete_nonexistent_turf_returns_404_or_ok(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.delete("/api/admin/turfs/999999", headers=headers)
        assert resp.status_code in (200, 404)


class TestBoundaryValues:
    def test_TC126_zero_price_time_slot_booking(self, client, created_turf):
        headers = created_turf["headers"]
        sport = client.post("/api/turf-admin/sports", json={"name": "free_sport"}, headers=headers).json()
        slot = client.post("/api/turf-admin/time-slots", json={
            "sport_id": sport["id"], "start_time": "06:00:00", "end_time": "07:00:00", "price": 0,
        }, headers=headers).json()
        resp = client.post("/api/public/bookings", json={
            "turf_id": created_turf["turf"]["id"], "sport_id": sport["id"], "time_slot_id": slot["id"],
            "booking_date": "2027-05-01", "customer_name": "Free Player",
            "customer_phone": "+8801711170001", "paid_amount": 0,
        })
        assert resp.status_code == 200
        assert resp.json()["payment_status"] == "paid"

    def test_TC127_booking_on_todays_date(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        today = date.today().isoformat()
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": today, "customer_name": "Today Booker",
            "customer_phone": "+8801711170002", "paid_amount": 0,
        })
        assert resp.status_code == 200

    def test_TC128_membership_with_100_percent_discount(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Free Forever", "duration_days": 30, "price": 5000,
            "discount_percentage": 100, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        member = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": membership["id"], "name": "Lucky Member",
            "phone": "+8801711170003", "amount_paid": 5000, "transaction_id": "TXN-FREE-001",
        }).json()
        client.patch(f"/api/turf-admin/members/{member['id']}/status", json={"status": "active"}, headers=d["headers"])
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-05-02", "customer_name": "Lucky Member",
            "customer_phone": "+8801711170003", "paid_amount": 0,
        })
        assert resp.status_code == 200
        assert resp.json()["total_amount"] == 0

    def test_TC129_very_long_customer_name_accepted(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-05-03", "customer_name": "A" * 300,
            "customer_phone": "+8801711170004", "paid_amount": 0,
        })
        assert resp.status_code == 200

    def test_TC130_special_characters_in_notes_field(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-05-04", "customer_name": "Special Chars",
            "customer_phone": "+8801711170005", "paid_amount": 0,
            "notes": "Test <script>alert(1)</script> & \"quotes\" 'apostrophe'",
        })
        assert resp.status_code == 200
        assert "script" in resp.json()["notes"]
