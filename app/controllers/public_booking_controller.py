from app.controllers.base_controller import BaseController
from app.schemas.booking_schema import BookingOut, PublicBookingCreate
from app.schemas.member_schema import MembershipCheckResult
from app.services.booking_service import BookingService
from app.services.member_service import MemberService


class PublicBookingController(BaseController[BookingService]):
    service_class = BookingService
