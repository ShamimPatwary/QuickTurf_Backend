from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.member_schema import MemberOut
from app.services.member_service import MemberService


class TurfAdminMemberController(BaseController[MemberService]):
    service_class = MemberService

    def list_members(self, turf_admin: TurfAdmin):
        return self.service.list_members(turf_admin)

    def get_member(self, turf_admin: TurfAdmin, member_id: int) -> MemberOut:
        return self.service.get_member(turf_admin, member_id)

    def update_member_status(self, turf_admin: TurfAdmin, member_id: int, new_status) -> MemberOut:
        return self.service.update_member_status(turf_admin, member_id, new_status)
