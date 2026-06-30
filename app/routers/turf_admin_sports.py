from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_sport_controller import TurfAdminSportController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.sport_schema import SportCreate, SportOut, SportUpdate

router = APIRouter(prefix="/api/turf-admin/sports", tags=["Turf Admin - Sports"])


@router.post("", response_model=SportOut)
def create_sport(
    data: SportCreate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminSportController(db).create_sport(turf_admin, data)


@router.get("", response_model=List[SportOut])
def list_sports(turf_admin: TurfAdmin = Depends(get_current_turf_admin), db: Session = Depends(get_db)):
    return TurfAdminSportController(db).list_sports(turf_admin)


@router.put("/{sport_id}", response_model=SportOut)
def update_sport(
    sport_id: int,
    data: SportUpdate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminSportController(db).update_sport(turf_admin, sport_id, data)


@router.delete("/{sport_id}")
def delete_sport(
    sport_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminSportController(db).delete_sport(turf_admin, sport_id)
