import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.config import settings
from app.models.booking import Booking


def generate_invoice_pdf(booking: Booking) -> str:
    folder_path = os.path.join(settings.UPLOAD_DIR, "invoices")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"invoice_{booking.id}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)