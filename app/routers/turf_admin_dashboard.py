from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.turf_admin_dashboard_controller import TurfAdminDashboardController
from app.core.dependencies import get_current_turf_admin
from app.database import get_db
from app.models.turf_admin import TurfAdmin
from app.schemas.booking_schema import DashboardStats

router = APIRouter(prefix="/api/turf-admin/dashboard", tags=["Turf Admin - Dashboard"])


@router.get("", response_model=DashboardStats)
def dashboard(turf_admin: TurfAdmin = Depends(get_current_turf_admin), db: Session = Depends(get_db)):
    return TurfAdminDashboardController(db).get_dashboard(turf_admin)
