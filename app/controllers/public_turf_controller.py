from datetime import date
from typing import Optional

from app.controllers.base_controller import BaseController
from app.services.public_turf_service import PublicTurfService


class PublicTurfController(BaseController[PublicTurfService]):
    service_class = PublicTurfService
    
    def browse_turfs(self, sport_name: Optional[str] = None):
        return self.service.browse_turfs(sport_name)

    def get_turf_detail(self, turf_id: int):
        return self.service.get_turf_detail(turf_id)

    def list_turf_sports(self, turf_id: int):
        return self.service.list_turf_sports(turf_id)

    def list_available_slots(self, turf_id: int, sport_id: int, booking_date: date):
        return self.service.list_available_slots(turf_id, sport_id, booking_date)

    def list_turf_packages(self, turf_id: int, sport_id: Optional[int] = None):
        return self.service.list_turf_packages(turf_id, sport_id)

    def list_turf_memberships(self, turf_id: int):
        return self.service.list_turf_memberships(turf_id)