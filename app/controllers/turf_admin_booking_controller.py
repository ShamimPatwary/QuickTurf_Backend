from typing import Optional

from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.booking_schema import BookingOut, BookingUpdate
from app.services.booking_service import BookingService
from app.services.whatsapp_service import WhatsAppService


class TurfAdminBookingController(BaseController[BookingService]):
    service_class = BookingService

    def list_bookings(self, turf_admin: TurfAdmin):
        return self.service.list_turf_bookings(turf_admin.turf_id)

    def get_booking(self, turf_admin: TurfAdmin, booking_id: int) -> BookingOut:
        return self.service.get_turf_booking(turf_admin.turf_id, booking_id)

    def update_booking(self, turf_admin: TurfAdmin, booking_id: int, data: BookingUpdate) -> BookingOut:
        return self.service.update_booking(turf_admin.turf_id, booking_id, data)

    def delete_booking(self, turf_admin: TurfAdmin, booking_id: int) -> dict:
        self.service.delete_booking(turf_admin.turf_id, booking_id)
        return {"detail": "Booking deleted"}

    def add_payment(
        self, turf_admin: TurfAdmin, booking_id: int, amount: float, method: str, transaction_id: Optional[str] = None
    ) -> BookingOut:
        return self.service.add_payment(turf_admin.turf_id, booking_id, amount, method, transaction_id)

    def confirm_and_get_whatsapp_link(self, turf_admin: TurfAdmin, booking_id: int) -> dict:
        booking = self.service.confirm_booking(turf_admin.turf_id, booking_id)
        link = WhatsAppService.build_whatsapp_link(booking)
        return {"whatsapp_link": link}
