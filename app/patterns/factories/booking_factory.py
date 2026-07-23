from app.models.booking import Booking, BookingStatus, MatchType, PaymentStatus
from app.models.time_slot import TimeSlot


class BookingFactory:
    """Builds a Booking entity with derived payment status and amounts."""

    @staticmethod
    def _resolve_payment_status(paid_amount: float, total_amount: float) -> PaymentStatus:
        if paid_amount <= 0:
            return PaymentStatus.PENDING
        if paid_amount >= total_amount:
            return PaymentStatus.PAID
        return PaymentStatus.PARTIAL