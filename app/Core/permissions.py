from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.turf import Turf, TurfStatus
from app.models.turf_admin import TurfAdmin


def ensure_turf_active(db: Session, turf_admin: TurfAdmin) -> Turf:
    turf = db.query(Turf).filter(Turf.id == turf_admin.turf_id).first()
    if not turf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turf not found")
    if turf.status == TurfStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Turf is suspended due to pending subscription payment",
        )
    return turf


def ensure_owns_turf(turf_admin: TurfAdmin, turf_id: int) -> None:
    if turf_admin.turf_id != turf_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this turf")
