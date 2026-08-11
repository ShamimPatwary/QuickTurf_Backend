"""tests/test_members.py — TC31-TC38: Membership purchase and approval workflow."""
import pytest


@pytest.fixture()
def turf_with_membership(client, turf_with_sport_and_slot):
    d = turf_with_sport_and_slot
    membership = client.post("/api/turf-admin/memberships", json={
        "name": "Test Membership", "duration_days": 30, "price": 2000,
        "discount_percentage": 10, "sport_ids": [d["sport"]["id"]],
    }, headers=d["headers"]).json()
    return {**d, "membership": membership}


class TestMembershipCreation:
    def test_TC31_create_membership_with_discount_and_sports(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post("/api/turf-admin/memberships", json={
            "name": "Premium", "duration_days": 30, "price": 3000,
            "discount_percentage": 25, "sport_ids": [d["sport"]["id"]],
        }, headers=d["headers"])
        assert resp.status_code == 200
        data = resp.json()
        assert data["discount_percentage"] == 25
        assert len(data["sports"]) == 1

    def test_TC32_membership_visible_on_public_turf_page(self, client, turf_with_membership):
        d = turf_with_membership
        resp = client.get(f"/api/public/turfs/{d['turf']['id']}/memberships")
        assert resp.status_code == 200
        assert d["membership"]["name"] in [m["name"] for m in resp.json()]


class TestMemberPurchase:
    def test_TC33_purchase_membership_creates_pending_record(self, client, turf_with_membership):
        d = turf_with_membership
        resp = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": d["membership"]["id"], "name": "New Member",
            "email": "newmember@test.com", "phone": "+8801811110001",
            "amount_paid": 2000, "transaction_id": "TXN-PURCHASE-001",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "pending"
        assert data["expires_at"] is None

    def test_TC34_purchase_requires_transaction_id(self, client, turf_with_membership):
        d = turf_with_membership
        resp = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": d["membership"]["id"], "name": "No TXN Member",
            "phone": "+8801811110002", "amount_paid": 2000,
        })
        assert resp.status_code == 422

    def test_TC35_purchase_for_nonexistent_membership_fails(self, client, turf_with_sport_and_slot):
        d = turf_with_sport_and_slot
        resp = client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": 99999, "name": "Ghost Member",
            "phone": "+8801811110003", "amount_paid": 1000, "transaction_id": "TXN-GHOST-001",
        })
        assert resp.status_code == 404


class TestMemberApproval:
    def _purchase(self, client, d, phone, tran_id):
        return client.post(f"/api/public/turfs/{d['turf']['id']}/memberships/purchase", json={
            "membership_id": d["membership"]["id"], "name": "Test Member",
            "phone": phone, "amount_paid": 2000, "transaction_id": tran_id,
        }).json()

    def test_TC36_approve_membership_sets_active_and_expiry(self, client, turf_with_membership):
        d = turf_with_membership
        member = self._purchase(client, d, "+8801811120001", "TXN-APPROVE-001")
        resp = client.patch(f"/api/turf-admin/members/{member['id']}/status",
                            json={"status": "active"}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["status"] == "active"
        assert resp.json()["expires_at"] is not None

    def test_TC37_reject_membership(self, client, turf_with_membership):
        d = turf_with_membership
        member = self._purchase(client, d, "+8801811120002", "TXN-REJECT-001")
        resp = client.patch(f"/api/turf-admin/members/{member['id']}/status",
                            json={"status": "rejected"}, headers=d["headers"])
        assert resp.status_code == 200
        assert resp.json()["status"] == "rejected"

    def test_TC38_list_members(self, client, turf_with_membership):
        d = turf_with_membership
        self._purchase(client, d, "+8801811120003", "TXN-LIST-001")
        resp = client.get("/api/turf-admin/members", headers=d["headers"])
        assert resp.status_code == 200
        assert len(resp.json()) >= 1
