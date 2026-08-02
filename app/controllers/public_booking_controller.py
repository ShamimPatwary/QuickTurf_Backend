from app.controllers.base_controller import BaseController
from app.schemas.booking_schema import BookingOut, PublicBookingCreate
from app.schemas.member_schema import MembershipCheckResult
from app.services.booking_service import BookingService
from app.services.member_service import MemberService


class PublicBookingController(BaseController[BookingService]):
    service_class = BookingService

    def create_booking(self, data: PublicBookingCreate) -> BookingOut:
        return self.service.create_public_booking(data)

    def check_discount(self, turf_id: int, phone: str, sport_id: int) -> MembershipCheckResult:
        member_service = MemberService(self.db)
        return member_service.check_membership_discount(turf_id, phone, sport_id)
