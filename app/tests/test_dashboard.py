"""tests/test_dashboard.py — TC39-TC45: Dashboard stats, packages, my-turf endpoint."""


class TestDashboard:
    def _make_booking(self, client, d, date, phone, paid=0):
        return client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": date, "customer_name": "Stat User", "customer_phone": phone, "paid_amount": paid,
        }).json()

    def test_TC39_dashboard_returns_all_fields(self, client, turf_with_sport_and_slot):
        resp = client.get("/api/turf-admin/dashboard", headers=turf_with_sport_and_slot["headers"])
        assert resp.status_code == 200
        data = resp.json()
        for field in ["total_matches", "total_match_amount", "paid_amount", "due_amount",
                      "upcoming_matches", "completed_matches", "cancelled_matches",
                      "payment_paid", "payment_partial", "payment_pending", "total_revenue",
                      "total_discount_given", "active_members", "pending_members"]:
            assert field in data

    def test_TC40_dashboard_counts_bookings(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        before = client.get("/api/turf-admin/dashboard", headers=d["headers"]).json()["total_matches"]
        self._make_booking(client, d, "2026-11-01", "+8801900000001")
        self._make_booking(client, d, "2026-11-02", "+8801900000002")
        after = client.get("/api/turf-admin/dashboard", headers=d["headers"]).json()["total_matches"]
        assert after == before + 2

    def test_TC41_dashboard_shows_active_members(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Stat Membership", "duration_days": 30, "price": 1000,
            "discount_percentage": 5, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        before = client.get("/api/turf-admin/dashboard", headers=d["headers"]).json()["active_members"]
        member = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": membership["id"], "name": "Stat Member",
            "phone": "+8801900000010", "amount_paid": 1000, "transaction_id": "TXN-STAT-001",
        }).json()
        client.patch(f"/api/turf-admin/members/{member['id']}/status",
                    json={"status": "active"}, headers=d["headers"])
        after = client.get("/api/turf-admin/dashboard", headers=d["headers"]).json()["active_members"]
        assert after == before + 1

    def test_TC42_dashboard_shows_discount_given(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Discount Stat", "duration_days": 30, "price": 1000,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        member = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": membership["id"], "name": "Discount User",
            "phone": "+8801900000020", "amount_paid": 1000, "transaction_id": "TXN-DISC-001",
        }).json()
        client.patch(f"/api/turf-admin/members/{member['id']}/status",
                    json={"status": "active"}, headers=d["headers"])
        before = client.get("/api/turf-admin/dashboard", headers=d["headers"]).json()["total_discount_given"]
        client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-11-05", "customer_name": "Discount User",
            "customer_phone": "+8801900000020", "paid_amount": 0,
        })
        after = client.get("/api/turf-admin/dashboard", headers=d["headers"]).json()["total_discount_given"]
        assert after == before + 100


class TestPackages:
    def test_TC43_create_package_with_sports(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/turf-admin/packages", json={
            "name": "Weekend Bundle", "description": "4 weekend sessions", "price": 3500,
            "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        assert resp.status_code == 200
        assert len(resp.json()["sports"]) == 1

    def test_TC44_package_visible_only_for_correct_sport(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        cricket = client.post("/api/turf-admin/sports", json={"name": "cricket_pkg_test"},
                              headers=d["headers"]).json()
        client.post("/api/turf-admin/packages", json={
            "name": "Football Only Pack", "price": 2000, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        resp_football = client.get(f"/api/public/turfs/{d['turf']['id']}/packages",
                                   params={"sport_id": d["sport"]["id"]})
        assert "Football Only Pack" in [p["name"] for p in resp_football.json()]
        resp_cricket = client.get(f"/api/public/turfs/{d['turf']['id']}/packages",
                                  params={"sport_id": cricket["id"]})
        assert "Football Only Pack" not in [p["name"] for p in resp_cricket.json()]


class TestMyTurf:
    def test_TC45_turf_admin_can_get_own_turf(self, client, created_turf):
        resp = client.get("/api/turf-admin/my-turf", headers=created_turf["headers"])
        assert resp.status_code == 200
        assert resp.json()["id"] == created_turf["turf"]["id"]
