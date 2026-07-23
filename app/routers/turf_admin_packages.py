from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_package_controller import TurfAdminPackageController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.package_schema import PackageCreate, PackageOut, PackageUpdate

router = APIRouter(prefix="/api/turf-admin/packages", tags=["Turf Admin - Packages"])


@router.post("", response_model=PackageOut)
def create_package(
    data: PackageCreate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminPackageController(db).create_package(turf_admin, data)


@router.get("", response_model=List[PackageOut])
def list_packages(turf_admin: TurfAdmin = Depends(get_current_turf_admin), db: Session = Depends(get_db)):
    return TurfAdminPackageController(db).list_packages(turf_admin)


@router.put("/{package_id}", response_model=PackageOut)
def update_package(
    package_id: int,
    data: PackageUpdate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminPackageController(db).update_package(turf_admin, package_id, data)


@router.delete("/{package_id}")
def delete_package(
    package_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminPackageController(db).delete_package(turf_admin, package_id)
