from app.patterns.observers.booking_subject import booking_subject
from app.patterns.observers.invoice_observer import InvoiceObserver
from app.patterns.observers.whatsapp_observer import WhatsAppObserver
from app.patterns.observers.dashboard_stats_observer import DashboardStatsObserver

booking_subject.attach(InvoiceObserver())
booking_subject.attach(WhatsAppObserver())
booking_subject.attach(DashboardStatsObserver())

__all__ = ["booking_subject"]
