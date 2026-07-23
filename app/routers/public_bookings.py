from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.controllers.public_booking_controller import PublicBookingController
from app.database import get_db
from app.schemas.booking_schema import BookingOut, PublicBookingCreate
from app.schemas.member_schema import MembershipCheckResult

router = APIRouter(prefix="/api/public/bookings", tags=["Public - Bookings"])


@router.post("", response_model=BookingOut)
def create_booking(data: PublicBookingCreate, db: Session = Depends(get_db)):
    return PublicBookingController(db).create_booking(data)


@router.get("/check-discount", response_model=MembershipCheckResult)
def check_discount(
    turf_id: int = Query(...),
    phone: str = Query(...),
    sport_id: int = Query(...),
    db: Session = Depends(get_db),
):
    return PublicBookingController(db).check_discount(turf_id, phone, sport_id)
