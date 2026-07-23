from app.controllers.base_controller import BaseController
from app.schemas.admin_schema import TokenResponse
from app.services.auth_service import AuthService


class PlatformAdminAuthController(BaseController[AuthService]):
    service_class = AuthService

    def login(self, email: str, password: str) -> TokenResponse:
        token = self.service.authenticate_admin(email, password)
        return TokenResponse(access_token=token, role="platform_admin")
