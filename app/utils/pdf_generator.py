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

    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "QuickTurf Booking Invoice")

    c.setFont("Helvetica", 11)
    lines = [
        f"Invoice #: {booking.id}",
        f"Customer Name: {booking.customer_name}",
        f"Phone: {booking.customer_phone}",
        f"Email: {booking.customer_email or '-'}",
        f"Booking Date: {booking.booking_date}",
        f"Total Amount: {booking.total_amount}",
        f"Paid Amount: {booking.paid_amount}",
        f"Due Amount: {booking.due_amount}",
        f"Payment Status: {booking.payment_status.value}",
        f"Notes: {booking.notes or '-'}",
    ]