from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException, status

from app.models.member import Member, MemberStatus
from app.models.turf import TurfStatus
from app.models.turf_admin import TurfAdmin
from app.repositories.member_repository import MemberRepository
from app.repositories.membership_repository import MembershipRepository
from app.repositories.turf_repository import TurfRepository
from app.schemas.member_schema import MemberPurchaseCreate, MembershipCheckResult
from app.services.base_service import BaseService

