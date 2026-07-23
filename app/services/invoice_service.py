import os

from fastapi import HTTPException, status

from app.config import settings
from app.repositories.booking_repository import BookingRepository
from app.services.base_service import BaseService
from app.utils.pdf_generator import generate_invoice_pdf