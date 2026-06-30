from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.controllers.invoice_controller import InvoiceController
from app.database import get_db

router = APIRouter(prefix="/api/invoices", tags=["Invoice"])


@router.get("/{booking_id}")
def download_invoice(booking_id: int, db: Session = Depends(get_db)):
    file_path = InvoiceController(db).get_invoice_path(booking_id)
    return FileResponse(file_path, media_type="application/pdf", filename=f"invoice_{booking_id}.pdf")
