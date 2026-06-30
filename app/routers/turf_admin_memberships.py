from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_membership_controller import TurfAdminMembershipController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.membership_schema import MembershipCreate, MembershipOut, MembershipUpdate

router = APIRouter(prefix="/api/turf-admin/memberships", tags=["Turf Admin - Memberships"])


@router.post("", response_model=MembershipOut)
def create_membership(
    data: MembershipCreate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminMembershipController(db).create_membership(turf_admin, data)


@router.get("", response_model=List[MembershipOut])
def list_memberships(turf_admin: TurfAdmin = Depends(get_current_turf_admin), db: Session = Depends(get_db)):
    return TurfAdminMembershipController(db).list_memberships(turf_admin)


@router.put("/{membership_id}", response_model=MembershipOut)
def update_membership(
    membership_id: int,
    data: MembershipUpdate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminMembershipController(db).update_membership(turf_admin, membership_id, data)


@router.delete("/{membership_id}")
def delete_membership(
    membership_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminMembershipController(db).delete_membership(turf_admin, membership_id)
