from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.sport_schema import SportCreate, SportOut, SportUpdate
from app.services.sport_service import SportService


class TurfAdminSportController(BaseController[SportService]):
    service_class = SportService

    def create_sport(self, turf_admin: TurfAdmin, data: SportCreate) -> SportOut:
        return self.service.create_sport(turf_admin, data)

    def list_sports(self, turf_admin: TurfAdmin):
        return self.service.list_sports(turf_admin)

    def update_sport(self, turf_admin: TurfAdmin, sport_id: int, data: SportUpdate) -> SportOut:
        return self.service.update_sport(turf_admin, sport_id, data)

    def delete_sport(self, turf_admin: TurfAdmin, sport_id: int) -> dict:
        self.service.delete_sport(turf_admin, sport_id)
        return {"detail": "Sport deleted"}
