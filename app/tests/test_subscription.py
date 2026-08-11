"""tests/test_subscription.py — TC46-TC50: 30-day auto-suspend subscription logic."""
from datetime import datetime, timedelta, timezone
from app.models.turf import Turf, TurfStatus
from app.services.subscription_service import suspend_expired_turfs


class TestSubscriptionWindow:
    def test_TC46_new_turf_gets_30_day_subscription(self, client, platform_admin_token):
        import uuid
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        email = f"sub_{uuid.uuid4().hex[:6]}@test.com"
        resp = client.post("/api/admin/turfs", json={
            "name": "Subscription Turf", "address": "1 Sub St",
            "turf_admin_email": email, "turf_admin_password": "pass123",
        }, headers=headers)
        assert resp.status_code == 200
        due_date = resp.json()["subscription_due_date"]
        assert due_date is not None
        due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        days_diff = (due - datetime.now(timezone.utc)).days
        assert 28 <= days_diff <= 30

    def test_TC47_activating_turf_resets_subscription_to_30_days(
            self, client, platform_admin_token, created_turf):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        resp = client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "active"}, headers=headers)
        assert resp.status_code == 200
        due_date = resp.json()["subscription_due_date"]
        due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        days_diff = (due - datetime.now(timezone.utc)).days
        assert 28 <= days_diff <= 30


class TestSubscriptionExpiryJob:
    def test_TC48_expired_active_turf_gets_suspended_by_job(
            self, client, platform_admin_token, created_turf, db):
        turf_id = created_turf["turf"]["id"]
        turf = db.query(Turf).filter(Turf.id == turf_id).first()
        turf.subscription_due_date = datetime.now(timezone.utc) - timedelta(days=1)
        turf.status = TurfStatus.ACTIVE
        db.commit()
        suspend_expired_turfs()
        refreshed = db.query(Turf).filter(Turf.id == turf_id).first()
        db.refresh(refreshed)
        assert refreshed.status == TurfStatus.SUSPENDED

    def test_TC49_non_expired_turf_not_touched_by_job(self, client, created_turf, db):
        turf_id = created_turf["turf"]["id"]
        turf = db.query(Turf).filter(Turf.id == turf_id).first()
        turf.subscription_due_date = datetime.now(timezone.utc) + timedelta(days=10)
        turf.status = TurfStatus.ACTIVE
        db.commit()
        suspend_expired_turfs()
        refreshed = db.query(Turf).filter(Turf.id == turf_id).first()
        db.refresh(refreshed)
        assert refreshed.status == TurfStatus.ACTIVE

    def test_TC50_already_suspended_turf_unaffected_by_job(
            self, client, platform_admin_token, created_turf, db):
        headers = {"Authorization": f"Bearer {platform_admin_token}"}
        turf_id = created_turf["turf"]["id"]
        client.patch(f"/api/admin/turfs/{turf_id}/status", json={"status": "suspended"}, headers=headers)
        suspend_expired_turfs()
        refreshed = db.query(Turf).filter(Turf.id == turf_id).first()
        db.refresh(refreshed)
        assert refreshed.status == TurfStatus.SUSPENDED
