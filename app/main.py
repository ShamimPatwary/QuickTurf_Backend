import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.services.subscription_service import suspend_expired_turfs
from apscheduler.schedulers.background import BackgroundScheduler


from app.config import settings
from app.patterns import observers  # noqa: F401 - registers concrete observers on import
from app.routers import (
    invoice,
    payment,
    platform_admin_auth,
    platform_admin_bookings,
    platform_admin_turfs,
    public_bookings,
    public_members,
    public_turfs,
    turf_admin_auth,
    turf_admin_bookings,
    turf_admin_dashboard,
    turf_admin_members,
    turf_admin_memberships,
    turf_admin_my_turf,
    turf_admin_packages,
    turf_admin_sports,
    turf_admin_time_slots,
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="QuickTurf API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(f"/{settings.UPLOAD_DIR}", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(platform_admin_auth.router)
app.include_router(platform_admin_turfs.router)
app.include_router(platform_admin_bookings.router)

app.include_router(turf_admin_my_turf.router)
app.include_router(turf_admin_auth.router)
app.include_router(turf_admin_sports.router)
app.include_router(turf_admin_time_slots.router)
app.include_router(turf_admin_packages.router)
app.include_router(turf_admin_memberships.router)
app.include_router(turf_admin_members.router)
app.include_router(turf_admin_bookings.router)
app.include_router(turf_admin_dashboard.router)

app.include_router(public_turfs.router)
app.include_router(public_bookings.router)
app.include_router(public_members.router)

app.include_router(payment.router)
app.include_router(invoice.router)


# ── Subscription scheduler ────────────────────────────────────────────────────
scheduler = BackgroundScheduler(timezone="Asia/Dhaka")
 
scheduler.add_job(
    suspend_expired_turfs,
    trigger="cron",
    hour=0,
    minute=5,
    id="suspend_expired_turfs",
    replace_existing=True,
)
 
 
@app.on_event("startup")
def start_scheduler():
    scheduler.start()
 
 
@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown(wait=False)

@app.get("/")
def root():
    return {"status": "QuickTurf API running"}
