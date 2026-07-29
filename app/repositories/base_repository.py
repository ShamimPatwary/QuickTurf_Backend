from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(ABC, Generic[ModelType]):
    """Abstract base defining the data-access contract for a single model type."""

    model: Type[ModelType]

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id_).first()

    def list_all(self) -> List[ModelType]:
        return self.db.query(self.model).all()

    