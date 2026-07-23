from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.public_member_controller import PublicMemberController
from app.database import get_db
from app.schemas.member_schema import MemberOut, MemberPurchaseCreate

router = APIRouter(prefix="/api/public/turfs", tags=["Public - Memberships"])


@router.post("/{turf_id}/memberships/purchase", response_model=MemberOut)
def purchase_membership(turf_id: int, data: MemberPurchaseCreate, db: Session = Depends(get_db)):
    return PublicMemberController(db).purchase_membership(turf_id, data)
