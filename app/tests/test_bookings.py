"""tests/test_bookings.py — TC19-TC30: Booking lifecycle, conflicts, payments, discounts."""


class TestBookingCreation:
    def test_TC19_create_booking_basic(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-01", "customer_name": "Karim Rahman",
            "customer_phone": "+8801711110001", "paid_amount": 0, "match_type": "friendly",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_amount"] == 1000
        assert data["payment_status"] == "pending"

    def test_TC20_booking_with_partial_payment(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-02", "customer_name": "Rahim",
            "customer_phone": "+8801711110002", "paid_amount": 500, "match_type": "practice",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["due_amount"] == 500
        assert data["payment_status"] == "partial"

    def test_TC21_booking_with_full_payment(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-03", "customer_name": "Jamal",
            "customer_phone": "+8801711110003", "paid_amount": 1000, "match_type": "tournament",
        })
        assert resp.status_code == 200
        assert resp.json()["payment_status"] == "paid"

    def test_TC22_booking_with_match_type(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-04", "customer_name": "Salam",
            "customer_phone": "+8801711110004", "paid_amount": 0, "match_type": "league",
        })
        assert resp.status_code == 200
        assert resp.json()["match_type"] == "league"

    def test_TC23_booking_with_transaction_id(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-05", "customer_name": "Hasan",
            "customer_phone": "+8801711110005", "paid_amount": 800, "transaction_id": "TXN-BKASH-9999",
        })
        assert resp.status_code == 200
        assert resp.json()["transaction_id"] == "TXN-BKASH-9999"


class TestBookingConflict:
    def test_TC24_double_booking_same_slot_same_date(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        payload = {
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-06", "customer_name": "First User",
            "customer_phone": "+8801711120001", "paid_amount": 0,
        }
        assert client.post("/api/public/bookings", json=payload).status_code == 200
        payload["customer_name"] = "Second User"
        payload["customer_phone"] = "+8801711120002"
        assert client.post("/api/public/bookings", json=payload).status_code == 409


class TestBookingManagement:
    def _create_booking(self, client, d, date, phone):
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": date, "customer_name": "Test Customer", "customer_phone": phone, "paid_amount": 0,
        })
        assert resp.status_code == 200
        return resp.json()

    def test_TC25_booking_shows_sport_name(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        self._create_booking(client, d, "2026-10-07", "+8801711130001")
        resp = client.get("/api/turf-admin/bookings", headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()[0]["sport_name"] == "football"

    def test_TC26_add_payment_with_transaction_id(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = self._create_booking(client, d, "2026-10-08", "+8801711130002")
        resp = client.post(f"/api/turf-admin/bookings/{booking['id']}/payments",
                           json={"amount": 1000, "method": "bkash", "transaction_id": "TXN-CROSS-001"},
                           headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["payment_status"] == "paid"
        assert resp.json()["transaction_id"] == "TXN-CROSS-001"

    def test_TC27_mark_booking_completed(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = self._create_booking(client, d, "2026-10-09", "+8801711130003")
        resp = client.put(f"/api/turf-admin/bookings/{booking['id']}",
                          json={"status": "completed"}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"

    def test_TC28_mark_booking_cancelled(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = self._create_booking(client, d, "2026-10-10", "+8801711130004")
        resp = client.put(f"/api/turf-admin/bookings/{booking['id']}",
                          json={"status": "cancelled"}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["status"] == "cancelled"


class TestMembershipDiscount:
    def test_TC29_membership_discount_auto_applied(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Gold Member", "duration_days": 30, "price": 2000,
            "discount_percentage": 20, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        member = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": membership["id"], "name": "VIP Customer",
            "phone": "+8801799999001", "amount_paid": 2000, "transaction_id": "TXN-MEM-GOLD",
        }).json()
        client.patch(f"/api/turf-admin/members/{member['id']}/status",
                    json={"status": "active"}, headers=d["headers"])
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-11", "customer_name": "VIP Customer",
            "customer_phone": "+8801799999001", "paid_amount": 0,
        })
        assert resp.status_code == 200
        assert resp.json()["discount_amount"] == 200.0
        assert resp.json()["total_amount"] == 800.0

    def test_TC29b_no_discount_for_pending_membership(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Silver Member", "duration_days": 30, "price": 1500,
            "discount_percentage": 15, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": membership["id"], "name": "Pending Customer",
            "phone": "+8801799999002", "amount_paid": 1500, "transaction_id": "TXN-MEM-PENDING",
        })
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-12", "customer_name": "Pending Customer",
            "customer_phone": "+8801799999002", "paid_amount": 0,
        })
        assert resp.status_code == 200
        assert resp.json()["discount_amount"] == 0


class TestBookingExtras:
    def test_TC30_whatsapp_link_generated(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-13", "customer_name": "WA Test",
            "customer_phone": "+8801711140001", "paid_amount": 0,
        }).json()
        resp = client.post(f"/api/turf-admin/bookings/{booking['id']}/confirm-whatsapp", headers=d["headers"])
        assert resp.status_code == 200
        assert "wa.me" in resp.json()["whatsapp_link"]

    def test_TC30b_invoice_download(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        booking = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-10-14", "customer_name": "Invoice Test",
            "customer_phone": "+8801711140002", "paid_amount": 500,
        }).json()
        resp = client.get(f"/api/invoices/{booking['id']}")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/pdf"
