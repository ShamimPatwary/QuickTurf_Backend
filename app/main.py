from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.patterns import observers  # noqa: F401 - registers concrete observers on import
from app.services.auth_service import seed_default_admin
from app.utils.migrate import run_migrations
from app.routers import (
    cron,
    invoice,
    payment,
    platform_admin_auth,
    platform_admin_bookings,
    platform_admin_contacts,
    platform_admin_turfs,
    public_bookings,
    public_contacts,
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure the DB schema is up to date (applies pending Alembic migrations,
    # e.g. the contact_messages table) before any data seeding. On Vercel
    # serverless this may not always run, so it is guarded and non-fatal.
    run_migrations()
    # Idempotently ensure the default platform admin exists (local/dev).
    # On Vercel serverless this may not always run, so authenticate_admin()
    # also seeds defensively on first login.
    try:
        seed_default_admin()
    except Exception:
        # Never block app startup on a seeding failure (e.g. DB down).
        pass
    yield


app = FastAPI(title="QuickTurf API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(public_contacts.router)

app.include_router(platform_admin_contacts.router)

app.include_router(payment.router)
app.include_router(invoice.router)

app.include_router(cron.router)

@app.get("/")
def root():
    return {"status": "QuickTurf API running"}
