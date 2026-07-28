from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.member_schema import MemberOut
from app.services.member_service import MemberService


class TurfAdminMemberController(BaseController[MemberService]):
    service_class = MemberService