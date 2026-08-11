import logging
from datetime import datetime, timezone
 
from sqlalchemy.orm import Session
 
from app.database import SessionLocal
from app.models.turf import Turf, TurfStatus
 
logger = logging.getLogger(__name__)
 
 
def suspend_expired_turfs() -> None:
    """
    Daily job: suspends any active turf whose subscription_due_date
    is in the past. Called automatically by APScheduler every day at 00:05.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
 
        expired_turfs = (
            db.query(Turf)
            .filter(
                Turf.status == TurfStatus.ACTIVE,
                Turf.subscription_due_date.isnot(None),
                Turf.subscription_due_date < now,
            )
            .all()
        )
 
        if not expired_turfs:
            logger.info("Subscription check: no expired turfs found.")
            return
 
        for turf in expired_turfs:
            turf.status = TurfStatus.SUSPENDED
            logger.warning(
                f"Turf '{turf.name}' (id={turf.id}) suspended — "
                f"subscription expired on {turf.subscription_due_date}"
            )
 
        db.commit()
        logger.info(
            f"Subscription check complete: {len(expired_turfs)} turf(s) suspended."
        )
 
    except Exception as e:
        db.rollback()
        logger.error(f"Subscription job failed: {e}")
    finally:
        db.close()
 