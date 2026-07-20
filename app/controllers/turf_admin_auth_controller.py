from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.admin_schema import TokenResponse
from app.services.auth_service import AuthService


class TurfAdminAuthController(BaseController[AuthService]):
    service_class = AuthService

    def login(self, email: str, password: str) -> TokenResponse:
        token = self.service.authenticate_turf_admin(email, password)
        return TokenResponse(access_token=token, role="turf_admin")

    def change_password(self, turf_admin: TurfAdmin, old_password: str, new_password: str) -> dict:
        self.service.change_turf_admin_password(turf_admin, old_password, new_password)
        return {"detail": "Password updated successfully"}
