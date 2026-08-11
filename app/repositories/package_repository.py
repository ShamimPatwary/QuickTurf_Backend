from typing import List, Optional

from app.models.package import Package
from app.models.sport import Sport
from app.repositories.base_repository import BaseRepository


class PackageRepository(BaseRepository[Package]):
    model = Package

    def list_by_turf(self, turf_id: int) -> List[Package]:
        return self.db.query(Package).filter(Package.turf_id == turf_id).all()

    def get_by_turf(self, package_id: int, turf_id: int) -> Optional[Package]:
        return self.db.query(Package).filter(Package.id == package_id, Package.turf_id == turf_id).first()

    
    def list_active_by_turf_and_sport(self, turf_id: int, sport_id: int) -> List[Package]:
        return (
            self.db.query(Package)
            .join(Package.sports)
            .filter(Package.turf_id == turf_id, Package.is_active == True, Sport.id == sport_id)  # noqa: E712
            .all()
        )
