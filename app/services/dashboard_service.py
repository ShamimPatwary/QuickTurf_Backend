from app.repositories.booking_repository import BookingRepository
from app.schemas.booking_schema import DashboardStats
from app.services.base_service import BaseService


class DashboardService(BaseService):
    """Aggregates turf admin dashboard statistics from booking records."""

    def __init__(self, db):
        super().__init__(db)
        self.booking_repo = BookingRepository(db)

    def get_turf_dashboard_stats(self, turf_id: int) -> DashboardStats:
        counts = self.booking_repo.turf_aggregate_counts(turf_id)
        return DashboardStats(
            total_matches=counts["total_matches"],
            total_match_amount=counts["total_match_amount"],
            paid_amount=counts["paid_amount"],
            due_amount=counts["due_amount"],
            upcoming_matches=counts["upcoming_matches"],
            completed_matches=counts["completed_matches"],
            cancelled_matches=counts["cancelled_matches"],
            payment_paid=counts["payment_paid"],
            payment_partial=counts["payment_partial"],
            payment_pending=counts["payment_pending"],
            total_revenue=counts["paid_amount"],
            total_discount_given=counts["total_discount_given"],
            active_members=counts["active_members"],
            pending_members=counts["pending_members"],
        )
