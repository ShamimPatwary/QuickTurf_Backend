from typing import List, Optional

from app.models.turf import Turf, TurfImage, TurfStatus
from app.repositories.base_repository import BaseRepository


class TurfRepository(BaseRepository[Turf]):
    model = Turf

    def list_active(self) -> List[Turf]:
        return self.db.query(Turf).filter(Turf.status == TurfStatus.ACTIVE).all()

    def add_image(self, turf_id: int, image_url: str) -> TurfImage:
        image = TurfImage(turf_id=turf_id, image_url=image_url)
        self.db.add(image)
        self.db.flush()
        return image

    