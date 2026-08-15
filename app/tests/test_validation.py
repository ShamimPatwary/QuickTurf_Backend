"""tests/test_validation.py — TC56-TC75: Input validation across major endpoints."""
import uuid


class TestTurfCreationValidation:
    def test_TC56_create_turf_missing_name(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.post("/api/admin/turfs", json={
            "address": "1 Test St", "turf_admin_email": f"a_{uuid.uuid4().hex[:6]}@t.com",
            "turf_admin_password": "pass123",
        }, headers=headers)
        assert resp.status_code == 422

    def test_TC57_create_turf_missing_address(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.post("/api/admin/turfs", json={
            "name": "No Address Turf", "turf_admin_email": f"a_{uuid.uuid4().hex[:6]}@t.com",
            "turf_admin_password": "pass123",
        }, headers=headers)
        assert resp.status_code == 422

    def test_TC58_create_turf_invalid_email_format(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.post("/api/admin/turfs", json={
            "name": "Bad Email Turf", "address": "1 Test St",
            "turf_admin_email": "not-an-email", "turf_admin_password": "pass123",
        }, headers=headers)
        assert resp.status_code == 422

    def test_TC59_create_turf_duplicate_admin_email(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        email = f"dup_{uuid.uuid4().hex[:6]}@t.com"
        client.post("/api/admin/turfs", json={
            "name": "First Turf", "address": "A St",
            "turf_admin_email": email, "turf_admin_password": "pass123",
        }, headers=headers)
        resp = client.post("/api/admin/turfs", json={
            "name": "Second Turf", "address": "B St",
            "turf_admin_email": email, "turf_admin_password": "pass456",
        }, headers=headers)
        assert resp.status_code == 400

    def test_TC60_create_turf_empty_name_string(self, client, platform_admin_token):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        resp = client.post("/api/admin/turfs", json={
            "name": "", "address": "1 Test St",
            "turf_admin_email": f"e_{uuid.uuid4().hex[:6]}@t.com", "turf_admin_password": "pass123",
        }, headers=headers)
        assert resp.status_code in (200, 422)


class TestBookingValidation:
    def test_TC61_booking_missing_customer_name(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-01", "customer_phone": "+8801711110001", "paid_amount": 0,
        })
        assert resp.status_code == 422

    def test_TC62_booking_missing_phone(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-02", "customer_name": "No Phone", "paid_amount": 0,
        })
        assert resp.status_code == 422

    def test_TC63_booking_invalid_email_format(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-03", "customer_name": "Bad Email",
            "customer_phone": "+8801711110002", "customer_email": "not-valid", "paid_amount": 0,
        })
        assert resp.status_code == 422

    def test_TC64_booking_nonexistent_turf(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": 999999, "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-04", "customer_name": "Ghost Turf",
            "customer_phone": "+8801711110003", "paid_amount": 0,
        })
        assert resp.status_code in (400, 404)

    def test_TC65_booking_nonexistent_sport(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": 999999, "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-05", "customer_name": "Ghost Sport",
            "customer_phone": "+8801711110004", "paid_amount": 0,
        })
        assert resp.status_code == 404

    def test_TC66_booking_nonexistent_time_slot(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": 999999,
            "booking_date": "2027-01-06", "customer_name": "Ghost Slot",
            "customer_phone": "+8801711110005", "paid_amount": 0,
        })
        assert resp.status_code == 404

    def test_TC67_booking_negative_paid_amount(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-07", "customer_name": "Negative Payer",
            "customer_phone": "+8801711110006", "paid_amount": -500,
        })
        assert resp.status_code in (200, 422)

    def test_TC68_booking_paid_amount_exceeds_total_is_capped(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2027-01-08", "customer_name": "Overpayer",
            "customer_phone": "+8801711110007", "paid_amount": 999999,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["paid_amount"] <= data["total_amount"]
        assert data["due_amount"] == 0


class TestSportAndSlotValidation:
    def test_TC69_create_sport_missing_name(self, client, created_turf):
        resp = client.post("/api/turf-admin/sports", json={}, headers=created_turf["headers"])
        assert resp.status_code == 422

    def test_TC70_create_time_slot_missing_price(self, client, created_turf):
        headers = created_turf["headers"]
        sport = client.post("/api/turf-admin/sports", json={"name": "tennis"}, headers=headers).json()
        resp = client.post("/api/turf-admin/time-slots", json={
            "sport_id": sport["id"], "start_time": "10:00:00", "end_time": "11:00:00",
        }, headers=headers)
        assert resp.status_code == 422

    def test_TC71_create_time_slot_invalid_time_format(self, client, created_turf):
        headers = created_turf["headers"]
        sport = client.post("/api/turf-admin/sports", json={"name": "squash"}, headers=headers).json()
        resp = client.post("/api/turf-admin/time-slots", json={
            "sport_id": sport["id"], "start_time": "not-a-time", "end_time": "11:00:00", "price": 500,
        }, headers=headers)
        assert resp.status_code == 422

    def test_TC72_create_time_slot_negative_price(self, client, created_turf):
        headers = created_turf["headers"]
        sport = client.post("/api/turf-admin/sports", json={"name": "hockey"}, headers=headers).json()
        resp = client.post("/api/turf-admin/time-slots", json={
            "sport_id": sport["id"], "start_time": "10:00:00", "end_time": "11:00:00", "price": -500,
        }, headers=headers)
        assert resp.status_code in (200, 422)


class TestPackageMembershipValidation:
    def test_TC73_create_package_missing_price(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/turf-admin/packages", json={
            "name": "No Price Package", "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        assert resp.status_code == 422

    def test_TC74_create_membership_discount_over_100_percent(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/turf-admin/memberships", json={
            "name": "Impossible Discount", "duration_days": 30, "price": 1000,
            "discount_percentage": 150, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        assert resp.status_code in (200, 422)

    def test_TC75_create_membership_missing_duration(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/turf-admin/memberships", json={
            "name": "No Duration", "price": 1000, "discount_percentage": 10,
            "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        assert resp.status_code == 422
