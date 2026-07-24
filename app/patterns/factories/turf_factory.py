from app.core.security import hash_password
from app.models.turf import Turf
from app.models.turf_admin import TurfAdmin
from app.schemas.turf_schema import TurfCreate


class TurfFactory:
    """Builds a Turf and its associated TurfAdmin from raw creation input."""

    @staticmethod
    def create_turf(data: TurfCreate) -> Turf:
        return Turf(
            name=data.name,
            details=data.details,
            address=data.address,
            
        )