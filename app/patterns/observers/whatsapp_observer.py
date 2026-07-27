from app.models.booking import Booking
from app.patterns.observers.observer_base import BookingObserver
from app.services.whatsapp_service import WhatsAppService


class WhatsAppObserver(BookingObserver):
    """Builds a WhatsApp share link with booking details once a booking is confirmed."""

    def on_booking_created(self, booking: Booking) -> None:
        pass

    def on_booking_confirmed(self, booking: Booking) -> None:
        WhatsAppService.build_whatsapp_link(booking)

        