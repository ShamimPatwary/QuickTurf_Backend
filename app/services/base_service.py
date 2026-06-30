from abc import ABC

from sqlalchemy.orm import Session


class BaseService(ABC):
    """Base class giving every service access to the current DB session."""

    def __init__(self, db: Session):
        self.db = db
