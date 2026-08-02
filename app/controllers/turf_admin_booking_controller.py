from typing import Optional

from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.booking_schema import BookingOut, BookingUpdate
from app.services.booking_service import BookingService
from app.services.whatsapp_service import WhatsAppService


class TurfAdminBookingController(BaseController[BookingService]):
    service_class = BookingService