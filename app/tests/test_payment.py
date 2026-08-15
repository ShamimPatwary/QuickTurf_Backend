"""tests/test_payment.py — TC51-TC55: SSLCommerz payment initiation (mocked, offline)."""
from unittest.mock import patch

MOCK_SUCCESS_RESPONSE = {
    "status": "SUCCESS",
    "GatewayPageURL": "https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=abc123",
    "sessionkey": "abc123",
}
MOCK_FAILURE_RESPONSE = {"status": "FAILED", "failedreason": "Invalid store credentials"}


class TestBookingPaymentInitiation:
    @patch("app.routers.payment.initiate_payment")
    def test_TC51_initiate_booking_payment_success(self, mock_initiate, client, turf_with_sport_and_slot):
        mock_initiate.return_value = MOCK_SUCCESS_RESPONSE
        d = turf_with_sport_and_slot
        booking = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-12-01", "customer_name": "Pay User",
            "customer_phone": "+8801755550001", "paid_amount": 0,
        }).json()
        resp = client.post(f"/api/payment/initiate/booking/{booking['id']}")
        assert resp.status_code == 200
        assert "gateway_url" in resp.json()

    def test_TC52_initiate_payment_nonexistent_booking(self, client):
        resp = client.post("/api/payment/initiate/booking/999999")
        assert resp.status_code == 404

    @patch("app.routers.payment.initiate_payment")
    def test_TC53_initiate_payment_sslcommerz_failure(self, mock_initiate, client, turf_with_sport_and_slot):
        mock_initiate.return_value = MOCK_FAILURE_RESPONSE
        d = turf_with_sport_and_slot
        booking = client.post("/api/public/bookings", json={
            "turf_id": d["turf"]["id"], "sport_id": d["sport"]["id"], "time_slot_id": d["slot"]["id"],
            "booking_date": "2026-12-02", "customer_name": "Fail User",
            "customer_phone": "+8801755550002", "paid_amount": 0,
        }).json()
        resp = client.post(f"/api/payment/initiate/booking/{booking['id']}")
        assert resp.status_code == 502


class TestMembershipPaymentInitiation:
    @patch("app.routers.payment.initiate_payment")
    def test_TC54_initiate_membership_payment_success(self, mock_initiate, client, turf_with_sport_and_slot):
        mock_initiate.return_value = MOCK_SUCCESS_RESPONSE
        d = turf_with_sport_and_slot
        membership = client.post("/api/turf-admin/memberships", json={
            "name": "Pay Test Membership", "duration_days": 30, "price": 1500,
            "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"]).json()
        resp = client.post("/api/payment/initiate/membership", json={
            "turf_id": d["turf"]["id"], "membership_id": membership["id"],
            "customer_name": "Membership Payer", "customer_phone": "+8801755550003",
        })
        assert resp.status_code == 200
        assert "gateway_url" in resp.json()

    def test_TC55_initiate_payment_nonexistent_membership(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/payment/initiate/membership", json={
            "turf_id": d["turf"]["id"], "membership_id": 999999,
            "customer_name": "Ghost Payer", "customer_phone": "+8801755550004",
        })
        assert resp.status_code == 404
