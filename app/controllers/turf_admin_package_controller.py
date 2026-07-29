from app.controllers.base_controller import BaseController
from app.models.turf_admin import TurfAdmin
from app.schemas.package_schema import PackageCreate, PackageOut, PackageUpdate
from app.services.package_service import PackageService


class TurfAdminPackageController(BaseController[PackageService]):
    service_class = PackageService

    def create_package(self, turf_admin: TurfAdmin, data: PackageCreate) -> PackageOut:
        return self.service.create_package(turf_admin, data)

    def list_packages(self, turf_admin: TurfAdmin):
        return self.service.list_packages(turf_admin)

    def update_package(self, turf_admin: TurfAdmin, package_id: int, data: PackageUpdate) -> PackageOut:
        return self.service.update_package(turf_admin, package_id, data)

    def delete_package(self, turf_admin: TurfAdmin, package_id: int) -> dict:
        self.service.delete_package(turf_admin, package_id)
        return {"detail": "Package deleted"}
