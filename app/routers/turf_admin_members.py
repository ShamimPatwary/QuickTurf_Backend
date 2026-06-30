from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_member_controller import TurfAdminMemberController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.member_schema import MemberOut, MemberStatusUpdate

router = APIRouter(prefix="/api/turf-admin/members", tags=["Turf Admin - Members"])


@router.get("", response_model=List[MemberOut])
def list_members(turf_admin: TurfAdmin = Depends(get_current_turf_admin), db: Session = Depends(get_db)):
    return TurfAdminMemberController(db).list_members(turf_admin)


@router.get("/{member_id}", response_model=MemberOut)
def get_member(
    member_id: int,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminMemberController(db).get_member(turf_admin, member_id)


@router.patch("/{member_id}/status", response_model=MemberOut)
def update_member_status(
    member_id: int,
    data: MemberStatusUpdate,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminMemberController(db).update_member_status(turf_admin, member_id, data.status)
