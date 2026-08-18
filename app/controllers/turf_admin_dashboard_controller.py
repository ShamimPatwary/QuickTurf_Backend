from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.booking_schema import DashboardStats
from app.services.dashboard_service import DashboardService


class TurfAdminDashboardController(BaseController[DashboardService]):
    service_class = DashboardService

    def get_dashboard(self, turf_admin: TurfAdmin) -> DashboardStats:
        return self.service.get_turf_dashboard_stats(turf_admin.turf_id)
