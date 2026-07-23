from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy.orm import Session

from app.services.base_service import BaseService

ServiceType = TypeVar("ServiceType", bound=BaseService)


class BaseController(ABC, Generic[ServiceType]):
    """Base class wiring a controller to its service, constructed from the request's DB session."""

    service_class: Type[ServiceType]

    def __init__(self, db: Session):
        self.db = db
        self.service: ServiceType = self.service_class(db)
