from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.membership_schema import MembershipCreate, MembershipOut, MembershipUpdate
from app.services.membership_service import MembershipService


class TurfAdminMembershipController(BaseController[MembershipService]):
    service_class = MembershipService
    
    def create_membership(self, turf_admin: TurfAdmin, data: MembershipCreate) -> MembershipOut:
        return self.service.create_membership(turf_admin, data)

    def list_memberships(self, turf_admin: TurfAdmin):
        return self.service.list_memberships(turf_admin)

    def update_membership(self, turf_admin: TurfAdmin, membership_id: int, data: MembershipUpdate) -> MembershipOut:
        return self.service.update_membership(turf_admin, membership_id, data)

    def delete_membership(self, turf_admin: TurfAdmin, membership_id: int) -> dict:
        self.service.delete_membership(turf_admin, membership_id)
        return {"detail": "Membership deleted"}
