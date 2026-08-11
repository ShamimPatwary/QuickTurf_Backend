"""tests/test_authorization.py — TC76-TC90: Cross-turf access boundaries and token security."""
import uuid


class TestCrossTurfAccessBlocked:
    def _second_turf(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        email = f"turf2_{uuid.uuid4().hex[:6]}@t.com"
        client.post("/api/admin/turfs", json={
            "name": "Second Turf", "address": "Other St",
            "turf_admin_email": email, "turf_admin_password": "pass123",
        }, headers=headers)
        login = client.post("/api/turf-admin/auth/login",
                            data={"username": email, "password": "pass123"})
        return {"Authorization": f"Bearer {login.json()['access_token']}"}

    def test_TC76_turf_b_cannot_see_turf_a_bookings(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-02-01", "customer_name": "Isolation Test",
            "customer_phone": "+8801711150001", "paid_amount": 0,
        })
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get("/api/turf-admin/bookings", headers=turf_b_headers)
        names = [b["customer_name"] for b in resp.json()]
        assert "Isolation Test" not in names

    def test_TC77_turf_b_cannot_view_turf_a_specific_booking(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-02-02", "customer_name": "Private Booking",
            "customer_phone": "+8801711150002", "paid_amount": 0,
        }).json()
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get(f"/api/turf-admin/bookings/{booking['id']}", headers=turf_b_headers)
        assert resp.status_code == 404

    def test_TC78_turf_b_cannot_add_payment_to_turf_a_booking(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-02-03", "customer_name": "Protected Booking",
            "customer_phone": "+8801711150003", "paid_amount": 0,
        }).json()
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.post(f"/api/turf-admin/bookings/{booking['id']}/payments",
                           json={"amount": 500, "method": "bkash"}, headers=turf_b_headers)
        assert resp.status_code == 404

    def test_TC79_turf_b_cannot_see_turf_a_sports(self, client, platform_admin_token, turf_with_sport_and_slot):
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get("/api/turf-admin/sports", headers=turf_b_headers)
        names = [s["name"] for s in resp.json()]
        assert "football" not in names

    def test_TC80_turf_b_cannot_modify_turf_a_time_slot(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.put(f"/api/turf-admin/time-slots/{d['slot']['id']}",
                          json={"price": 1}, headers=turf_b_headers)
        assert resp.status_code == 404

    def test_TC81_turf_b_cannot_see_turf_a_packages(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.post("/api/turf-admin/packages", json={
            "name": "Private Package", "price": 1000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get("/api/turf-admin/packages", headers=turf_b_headers)
        names = [p["name"] for p in resp.json()]
        assert "Private Package" not in names

    def test_TC82_turf_b_cannot_see_turf_a_memberships(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.post("/api/turf-admin/memberships", json={
            "name": "Private Membership", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get("/api/turf-admin/memberships", headers=turf_b_headers)
        names = [m["name"] for m in resp.json()]
        assert "Private Membership" not in names

    def test_TC83_turf_b_cannot_see_turf_a_members(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Membership For Isolation", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": membership["id"], "name": "Isolated Member",
            "phone": "+8801711150004", "amount_paid": 1000, "transaction_id": "TXN-ISO-001",
        })
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get("/api/turf-admin/members", headers=turf_b_headers)
        names = [m["name"] for m in resp.json()]
        assert "Isolated Member" not in names

    def test_TC84_turf_b_dashboard_does_not_include_turf_a_stats(self, client, platform_admin_token, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-02-04", "customer_name": "Dashboard Isolation",
            "customer_phone": "+8801711150005", "paid_amount": 1000,
        })
        turf_b_headers = self._second_turf(client, platform_admin_token)
        resp = client.get("/api/turf-admin/dashboard", headers=turf_b_headers)
        assert resp.json()["total_matches"] == 0


class TestTokenSecurity:
    def test_TC85_turf_admin_token_rejected_on_platform_admin_route(self, client, created_turf):
        resp = client.get("/api/admin/turfs", headers=created_turf["headers"])
        assert resp.status_code == 401

    def test_TC86_platform_admin_token_rejected_on_turf_admin_route(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.get("/api/turf-admin/bookings", headers=headers)
        assert resp.status_code == 401

    def test_TC87_malformed_authorization_header(self, client):
        resp = client.get("/api/admin/turfs", headers={"Authorization": "NotBearer sometoken"})
        assert resp.status_code == 401

    def test_TC88_empty_bearer_token(self, client):
        resp = client.get("/api/admin/turfs", headers={"Authorization": "Bearer "})
        assert resp.status_code == 401

    def test_TC89_tampered_jwt_signature_rejected(self, client, platform_admin_token):
        tampered = platform_admin_token[:-5] + "AAAAA"
        resp = client.get("/api/admin/turfs", headers={"Authorization": f"Bearer {tampered}"})
        assert resp.status_code == 401

    def test_TC90_change_password_without_auth_header(self, client):
        resp = client.post("/api/turf-admin/auth/change-password",
                           json={"old_password": "a", "new_password": "b"})
        assert resp.status_code == 401
