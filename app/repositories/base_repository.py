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

  

    def add(self, instance: ModelType) -> ModelType:
        self.db.add(instance)
        self.db.flush()
        return instance

    def delete(self, instance: ModelType) -> None:
        self.db.delete(instance)

    def commit(self) -> None:
        self.db.commit()

    def refresh(self, instance: ModelType) -> None:
        self.db.refresh(instance)
