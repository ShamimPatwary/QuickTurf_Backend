from typing import List, Optional

from app.models.sport import Sport
from app.repositories.base_repository import BaseRepository


class SportRepository(BaseRepository[Sport]):
    model = Sport

    def list_by_turf(self, turf_id: int) -> List[Sport]:
        return self.db.query(Sport).filter(Sport.turf_id == turf_id).all()

    def get_by_turf(self, sport_id: int, turf_id: int) -> Optional[Sport]:
        return self.db.query(Sport).filter(Sport.id == sport_id, Sport.turf_id == turf_id).first()
