from abc import ABC, abstractmethod

from app.models.booking import Booking

class BookingObserver(ABC):
    """Interface every concrete booking observer must implement."""

    @abstractmethod
    def on_booking_created(self, booking: Booking) -> None:
        ...

    @abstractmethod
    def on_booking_confirmed(self, booking: Booking) -> None:
        ...

