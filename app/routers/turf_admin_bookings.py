from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_booking_controller import TurfAdminBookingController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.booking_schema import BookingAddPayment, BookingOut, BookingUpdate

router = APIRouter(prefix="/api/turf-admin/bookings", tags=["Turf Admin - Bookings"])


@router.get("", response_model=List[BookingOut])
def list_bookings(turf_admin: TurfAdmin = Depends(get_current_turf_admin), db: Session = Depends(get_db)):
    return TurfAdminBookingController(db).list_bookings(turf_admin)


@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(
    booking_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminBookingController(db).get_booking(turf_admin, booking_id)


@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(
    booking_id: int,
    data: BookingUpdate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminBookingController(db).update_booking(turf_admin, booking_id, data)


@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminBookingController(db).delete_booking(turf_admin, booking_id)


@router.post("/{booking_id}/payments", response_model=BookingOut)
def add_payment(
    booking_id: int,
    data: BookingAddPayment,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminBookingController(db).add_payment(
        turf_admin, booking_id, data.amount, data.method, data.transaction_id
    )


@router.post("/{booking_id}/confirm-whatsapp")
def confirm_and_get_whatsapp_link(
    booking_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminBookingController(db).confirm_and_get_whatsapp_link(turf_admin, booking_id)
