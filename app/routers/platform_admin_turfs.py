from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.controllers.platform_admin_turf_controller import PlatformAdminTurfController
from app.core.dependencies import get_current_admin
from app.database import get_db
from app.schemas.turf_schema import TurfCreate, TurfImageOut, TurfOut, TurfStatusUpdate, TurfUpdate

router = APIRouter(prefix="/api/admin/turfs", tags=["Platform Admin - Turfs"])


@router.post("", response_model=TurfOut, dependencies=[Depends(get_current_admin)])
def create_turf(data: TurfCreate, db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).create_turf(data)


@router.get("", response_model=List[TurfOut], dependencies=[Depends(get_current_admin)])
def list_turfs(db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).list_turfs()


@router.get("/{turf_id}", response_model=TurfOut, dependencies=[Depends(get_current_admin)])
def get_turf(turf_id: int, db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).get_turf(turf_id)


@router.put("/{turf_id}", response_model=TurfOut, dependencies=[Depends(get_current_admin)])
def update_turf(turf_id: int, data: TurfUpdate, db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).update_turf(turf_id, data)


@router.delete("/{turf_id}", dependencies=[Depends(get_current_admin)])
def delete_turf(turf_id: int, db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).delete_turf(turf_id)


@router.patch("/{turf_id}/status", response_model=TurfOut, dependencies=[Depends(get_current_admin)])
def update_turf_status(turf_id: int, data: TurfStatusUpdate, db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).update_turf_status(turf_id, data.status, data.subscription_due_date)


@router.post("/{turf_id}/images", response_model=TurfImageOut, dependencies=[Depends(get_current_admin)])
def upload_turf_image(turf_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).upload_turf_image(turf_id, file)


@router.delete("/{turf_id}/images/{image_id}", dependencies=[Depends(get_current_admin)])
def delete_turf_image(turf_id: int, image_id: int, db: Session = Depends(get_db)):
    return PlatformAdminTurfController(db).delete_turf_image(turf_id, image_id)
