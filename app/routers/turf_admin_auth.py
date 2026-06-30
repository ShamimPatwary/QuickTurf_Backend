from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controllers.turf_admin_auth_controller import TurfAdminAuthController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.admin_schema import TokenResponse
from app.schemas.turf_admin_schema import TurfAdminChangePassword

router = APIRouter(prefix="/api/turf-admin/auth", tags=["Turf Admin Auth"])


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return TurfAdminAuthController(db).login(form_data.username, form_data.password)


@router.post("/change-password")
def change_password(
    data: TurfAdminChangePassword,
    turf_admin: TurfAdmin = Depends(get_current_turf_admin),
    db: Session = Depends(get_db),
):
    return TurfAdminAuthController(db).change_password(turf_admin, data.old_password, data.new_password)
