from typing import List

from fastapi import HTTPException, status

from app.core.permissions import ensure_turf_active
from app.models.membership import Membership
from app.models.turf_admin import TurfAdmin
from app.repositories.membership_repository import MembershipRepository
from app.schemas.membership_schema import MembershipCreate, MembershipUpdate
from app.services.base_service import BaseService

class MembershipService(BaseService):
    """Turf-admin facing business logic for managing memberships."""
