from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.package_schema import PackageCreate, PackageOut, PackageUpdate
from app.services.package_service import PackageService


class TurfAdminPackageController(BaseController[PackageService]):
    service_class = PackageService
