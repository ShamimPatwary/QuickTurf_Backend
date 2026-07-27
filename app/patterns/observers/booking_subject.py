from typing import List

from app.models.booking import Booking
from app.patterns.observers.observer_base import BookingObserver


class BookingSubject:
    """Maintains a list of observers and notifies them of booking lifecycle events."""

    def __init__(self) -> None:
        self._observers: List[BookingObserver] = []

      def attach(self, observer: BookingObserver) -> None:
        self._observers.append(observer)