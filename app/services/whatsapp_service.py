import urllib.parse

from app.models.booking import Booking


class WhatsAppService:
    """Builds wa.me deep links with prefilled booking details."""


    @staticmethod
    def build_whatsapp_link(booking: Booking) -> str:
        message = (
            f"Hello {booking.customer_name},\n"
            f"Your booking is confirmed.\n"
            f"Date: {booking.booking_date}\n"
            f"Total Amount: {booking.total_amount}\n"
            f"Paid: {booking.paid_amount}\n"
            f"Due: {booking.due_amount}\n"
            f"Notes: {booking.notes or '-'}\n"
            f"Thank you for booking with QuickTurf!"
        )

        phone = booking.customer_phone.replace("+", "").replace(" ", "")
        encoded_message = urllib.parse.quote(message)

        return f"https://wa.me/{phone}?text={encoded_message}"
