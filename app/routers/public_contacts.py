from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.contact_controller import ContactController
from app.database import get_db
from app.schemas.contact_schema import ContactMessageCreate, ContactMessageOut

router = APIRouter(prefix="/api/public/contact-messages", tags=["Public - Contact Messages"])


@router.post("", response_model=ContactMessageOut)
def create_contact_message(data: ContactMessageCreate, db: Session = Depends(get_db)):
    return ContactController(db).create_message(data)
