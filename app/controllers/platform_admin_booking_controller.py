from app.controllers.base_controller import BaseController
from app.services.booking_service import BookingService


class PlatformAdminBookingController(BaseController[BookingService]):
    service_class = BookingService

    def list_bookings(self):
        return self.service.list_all_bookings_for_platform()
