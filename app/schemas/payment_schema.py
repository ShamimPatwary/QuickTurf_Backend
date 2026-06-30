from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaymentOut(BaseModel):
    id: int
    booking_id: int
    amount: float
    method: Optional[str]
    transaction_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
