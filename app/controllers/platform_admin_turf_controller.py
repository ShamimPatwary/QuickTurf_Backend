from fastapi import UploadFile

from app.controllers.base_controller import BaseController
from app.schemas.turf_schema import TurfCreate, TurfImageOut, TurfOut, TurfUpdate
from app.services.turf_service import TurfService
from app.utils.file_upload import save_upload


class PlatformAdminTurfController(BaseController[TurfService]):
    service_class = TurfService

    def create_turf(self, data: TurfCreate) -> TurfOut:
        return self.service.create_turf(data)

    def list_turfs(self):
        return self.service.list_turfs()

    def get_turf(self, turf_id: int) -> TurfOut:
        return self.service.get_turf(turf_id)

    def update_turf(self, turf_id: int, data: TurfUpdate) -> TurfOut:
        return self.service.update_turf(turf_id, data)

    def delete_turf(self, turf_id: int) -> dict:
        self.service.delete_turf(turf_id)
        return {"detail": "Turf deleted"}

    def update_turf_status(self, turf_id: int, status_value, subscription_due_date=None) -> TurfOut:
        return self.service.update_turf_status(turf_id, status_value, subscription_due_date)

    def upload_turf_image(self, turf_id: int, file: UploadFile) -> TurfImageOut:
        image_url = save_upload(file)
        return self.service.add_turf_image(turf_id, image_url)

    def delete_turf_image(self, turf_id: int, image_id: int) -> dict:
        self.service.delete_turf_image(turf_id, image_id)
        return {"detail": "Image deleted"}
