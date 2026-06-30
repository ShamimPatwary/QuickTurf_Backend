from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_time_slot_controller import TurfAdminTimeSlotController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.time_slot_schema import TimeSlotCreate, TimeSlotOut, TimeSlotUpdate

router = APIRouter(prefix="/api/turf-admin/time-slots", tags=["Turf Admin - Time Slots"])


@router.post("", response_model=TimeSlotOut)
def create_time_slot(
    data: TimeSlotCreate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminTimeSlotController(db).create_time_slot(turf_admin, data)


@router.get("", response_model=List[TimeSlotOut])
def list_time_slots(
    sport_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminTimeSlotController(db).list_time_slots(turf_admin, sport_id)


@router.put("/{time_slot_id}", response_model=TimeSlotOut)
def update_time_slot(
    time_slot_id: int,
    data: TimeSlotUpdate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminTimeSlotController(db).update_time_slot(turf_admin, time_slot_id, data)


@router.delete("/{time_slot_id}")
def delete_time_slot(
    time_slot_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminTimeSlotController(db).delete_time_slot(turf_admin, time_slot_id)
