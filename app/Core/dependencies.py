from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.admin import Admin
from app.models.turf_admin import TurfAdmin

platform_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/auth/login")
turf_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/turf-admin/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_admin(
    token: str = Depends(platform_oauth2_scheme), db: Session = Depends(get_db)
) -> Admin:
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "platform_admin":
        raise credentials_exception

    admin_id = payload.get("sub")
    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    if not admin:
        raise credentials_exception
    return admin


def get_current_turf_admin(
    token: str = Depends(turf_oauth2_scheme), db: Session = Depends(get_db)
) -> TurfAdmin:
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "turf_admin":
        raise credentials_exception

    turf_admin_id = payload.get("sub")
    turf_admin = db.query(TurfAdmin).filter(TurfAdmin.id == int(turf_admin_id)).first()
    if not turf_admin:
        raise credentials_exception
    return turf_admin
