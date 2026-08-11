from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.time_slot_schema import TimeSlotCreate, TimeSlotOut, TimeSlotUpdate
from app.services.time_slot_service import TimeSlotService


class TurfAdminTimeSlotController(BaseController[TimeSlotService]):
    service_class = TimeSlotService

    def create_time_slot(self, turf_admin: TurfAdmin, data: TimeSlotCreate) -> TimeSlotOut:
        return self.service.create_time_slot(turf_admin, data)

    def list_time_slots(self, turf_admin: TurfAdmin, sport_id: int):
        return self.service.list_time_slots(turf_admin, sport_id)

    def update_time_slot(self, turf_admin: TurfAdmin, time_slot_id: int, data: TimeSlotUpdate) -> TimeSlotOut:
        return self.service.update_time_slot(turf_admin, time_slot_id, data)

    def delete_time_slot(self, turf_admin: TurfAdmin, time_slot_id: int) -> dict:
        self.service.delete_time_slot(turf_admin, time_slot_id)
        return {"detail": "Time slot deleted"}
