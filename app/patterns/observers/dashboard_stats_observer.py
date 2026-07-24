from app.models.booking import Booking
from app.patterns.observers.observer_base import BookingObserver

class DashboardStatsObserver(BookingObserver):
    """Hook point for recomputing/caching turf dashboard stats on booking events."""

    def on_booking_created(self, booking: Booking) -> None:
        pass

    def on_booking_confirmed(self, booking: Booking) -> None:
        pass
