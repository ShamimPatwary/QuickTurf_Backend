from datetime import time
from typing import Optional

from pydantic import BaseModel


class TimeSlotCreate(BaseModel):
    sport_id: int
    start_time: time
    end_time: time
    price: float





class TimeSlotOut(BaseModel):
    id: int
    sport_id: int
    start_time: time
    end_time: time
    price: float
    is_active: bool

    class Config:
        from_attributes = True


class AvailableTimeSlotOut(BaseModel):
    id: int
    start_time: time
    end_time: time
    price: float
    is_booked: bool

    class Config:
        from_attributes = True
