"""
NEW FILE: app/services/sslcommerz_service.py

Handles all communication with the SSLCommerz API:
  - initiate_payment()  → gets GatewayPageURL to redirect user
  - validate_payment()  → verifies the transaction after redirect back
"""
import uuid
from typing import Optional

import requests

from app.config import settings


SANDBOX_API = "https://sandbox.sslcommerz.com"
LIVE_API = "https://securepay.sslcommerz.com"


def _base_url() -> str:
    return SANDBOX_API if settings.SSLCOMMERZ_IS_SANDBOX else LIVE_API


def initiate_payment(
    amount: float,
    currency: str = "BDT",
    tran_id: Optional[str] = None,
    product_name: str = "QuickTurf Booking",
    product_category: str = "Sports",
    customer_name: str = "Customer",
    customer_email: str = "customer@example.com",
    customer_phone: str = "01700000000",
    customer_address: str = "Dhaka, Bangladesh",
    extra_payload: Optional[dict] = None,  # stored as value1..value4 for later retrieval
) -> dict:
    """
    Call SSLCommerz /gwprocess/v4/api.php to create a payment session.
    Returns the full API response dict which includes GatewayPageURL.
    Raises on network or API error.
    """
    if not tran_id:
        tran_id = str(uuid.uuid4())

    payload = {
        "store_id": settings.SSLCOMMERZ_STORE_ID,
        "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
        "total_amount": str(amount),
        "currency": currency,
        "tran_id": tran_id,
        "success_url": settings.SSLCOMMERZ_SUCCESS_URL,
        "fail_url": settings.SSLCOMMERZ_FAIL_URL,
        "cancel_url": settings.SSLCOMMERZ_CANCEL_URL,
        "ipn_url": f"{settings.BASE_URL}/api/payment/ipn",
        "product_name": product_name,
        "product_category": product_category,
        "product_profile": "general",
        "cus_name": customer_name,
        "cus_email": customer_email,
        "cus_phone": customer_phone,
        "cus_add1": customer_address,
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "ship_name": customer_name,
        "ship_add1": customer_address,
        "ship_city": "Dhaka",
        "ship_country": "Bangladesh",
        "shipping_method": "NO",
        "num_of_item": 1,
    }

    # Pack any extra info into value1..value4 so we can retrieve it on callback
    if extra_payload:
        items = list(extra_payload.items())
        for i, (k, v) in enumerate(items[:4]):
            payload[f"value{i+1}"] = str(v)

    url = f"{_base_url()}/gwprocess/v4/api.php"
    response = requests.post(url, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def validate_payment(val_id: str) -> dict:
    """
    Validate a payment using the val_id returned by SSLCommerz on success.
    Returns the validation response dict.
    """
    url = f"{_base_url()}/validator/api/validationserverAPI.php"
    params = {
        "val_id": val_id,
        "store_id": settings.SSLCOMMERZ_STORE_ID,
        "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
        "format": "json",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
