from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controllers.platform_admin_auth_controller import PlatformAdminAuthController
from app.database import get_db
from app.schemas.admin_schema import TokenResponse

router = APIRouter(prefix="/api/admin/auth", tags=["Platform Admin Auth"])


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    controller = PlatformAdminAuthController(db)
    return controller.login(form_data.username, form_data.password)
