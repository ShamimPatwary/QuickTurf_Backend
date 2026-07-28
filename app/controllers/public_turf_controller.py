from datetime import date
from typing import Optional

from app.controllers.base_controller import BaseController
from app.services.public_turf_service import PublicTurfService


class PublicTurfController(BaseController[PublicTurfService]):
    service_class = PublicTurfService
