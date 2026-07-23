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


    @classmethod
    def create_booking(
        cls,
        turf_id: int,
        sport_id: int,
        time_slot: TimeSlot,
        booking_date,
        customer_name: str,
        customer_phone: str,
        customer_email: str | None,
        paid_amount: float,
        notes: str | None,
        match_type: MatchType = MatchType.FRIENDLY,
        transaction_id: str | None = None,
        discount_percentage: float = 0,
    ) -> Booking:
        base_amount = time_slot.price
        discount_amount = round(base_amount * (discount_percentage / 100), 2) if discount_percentage else 0
        total_amount = max(base_amount - discount_amount, 0)

        paid_amount = min(paid_amount, total_amount)
        due_amount = total_amount - paid_amount


        return Booking(
            turf_id=turf_id,
            sport_id=sport_id,
            time_slot_id=time_slot.id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            booking_date=booking_date,
            notes=notes,
            match_type=match_type,
            transaction_id=transaction_id,
            total_amount=total_amount,
            discount_amount=discount_amount,
            paid_amount=paid_amount,
            due_amount=due_amount,
            status=BookingStatus.UPCOMING,
            payment_status=cls._resolve_payment_status(paid_amount, total_amount),
        )
