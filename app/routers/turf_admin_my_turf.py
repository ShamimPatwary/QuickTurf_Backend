from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf import Turf
from app.models.turf_admin import TurfAdmin
from app.schemas.turf_schema import TurfPublicOut

router = APIRouter(prefix="/api/turf-admin", tags=["Turf Admin - My Turf"])
