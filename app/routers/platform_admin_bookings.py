from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.platform_admin_booking_controller import PlatformAdminBookingController
from app.core.dependencies import get_current_admin
from app.database import get_db
from app.schemas.booking_schema import BookingOut

router = APIRouter(prefix="/api/admin/bookings", tags=["Platform Admin - Bookings"])


@router.get("", response_model=List[BookingOut], dependencies=[Depends(get_current_admin)])
def list_bookings(db: Session = Depends(get_db)):
    return PlatformAdminBookingController(db).list_bookings()
