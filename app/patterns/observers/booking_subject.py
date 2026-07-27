from typing import List

from app.models.booking import Booking
from app.patterns.observers.observer_base import BookingObserver


class BookingSubject:
    """Maintains a list of observers and notifies them of booking lifecycle events."""

    def __init__(self) -> None:
        self._observers: List[BookingObserver] = []

    def attach(self, observer: BookingObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: BookingObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_created(self, booking: Booking) -> None:
        for observer in self._observers:
            observer.on_booking_created(booking)

    def notify_confirmed(self, booking: Booking) -> None:
        for observer in self._observers:
            observer.on_booking_confirmed(booking)


booking_subject = BookingSubject()
