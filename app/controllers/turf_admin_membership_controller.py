from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.membership_schema import MembershipCreate, MembershipOut, MembershipUpdate
from app.services.membership_service import MembershipService


class TurfAdminMembershipController(BaseController[MembershipService]):
    service_class = MembershipService
