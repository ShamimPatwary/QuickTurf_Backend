import urllib.parse

from app.models.booking import Booking


class WhatsAppService:
    """Builds wa.me deep links with prefilled booking details."""
