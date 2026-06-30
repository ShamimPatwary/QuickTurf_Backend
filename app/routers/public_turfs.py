from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.controllers.public_turf_controller import PublicTurfController
from app.database import get_db
from app.schemas.membership_schema import MembershipOut
from app.schemas.package_schema import PackageOut
from app.schemas.sport_schema import SportOut
from app.schemas.time_slot_schema import AvailableTimeSlotOut
from app.schemas.turf_schema import TurfPublicOut

router = APIRouter(prefix="/api/public/turfs", tags=["Public - Turfs"])


@router.get("", response_model=List[TurfPublicOut])
def browse_turfs(
    sport_name: str = Query(None, description="Filter turfs offering this sport, e.g. football or cricket"),
    db: Session = Depends(get_db),
):
    return PublicTurfController(db).browse_turfs(sport_name)


@router.get("/{turf_id}", response_model=TurfPublicOut)
def get_turf_detail(turf_id: int, db: Session = Depends(get_db)):
    return PublicTurfController(db).get_turf_detail(turf_id)


@router.get("/{turf_id}/sports", response_model=List[SportOut])
def list_turf_sports(turf_id: int, db: Session = Depends(get_db)):
    return PublicTurfController(db).list_turf_sports(turf_id)


@router.get("/{turf_id}/sports/{sport_id}/available-slots", response_model=List[AvailableTimeSlotOut])
def list_available_slots(
    turf_id: int,
    sport_id: int,
    booking_date: date = Query(..., description="Date to check slot availability for"),
    db: Session = Depends(get_db),
):
    return PublicTurfController(db).list_available_slots(turf_id, sport_id, booking_date)


@router.get("/{turf_id}/packages", response_model=List[PackageOut])
def list_turf_packages(
    turf_id: int,
    sport_id: Optional[int] = Query(None, description="Filter packages that apply to this sport"),
    db: Session = Depends(get_db),
):
    return PublicTurfController(db).list_turf_packages(turf_id, sport_id)


@router.get("/{turf_id}/memberships", response_model=List[MembershipOut])
def list_turf_memberships(turf_id: int, db: Session = Depends(get_db)):
    return PublicTurfController(db).list_turf_memberships(turf_id)
