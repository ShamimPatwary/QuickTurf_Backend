"""Run Alembic migrations programmatically on app startup.

On Vercel serverless, functions are spun up per request and the FastAPI
lifespan does not reliably run CLI migration commands. This helper applies
any pending migrations (e.g. `alembic upgrade head`) at startup using the
configured DATABASE_URL, so the schema stays in sync without manual steps.

Guarded so a migration failure logs a warning but never blocks startup.
"""
import logging
from pathlib import Path

from alembic import command
from alembic.config import Config

from app.config import settings

logger = logging.getLogger(__name__)

# Alembic reads the ini relative to the backend project root.
_BACKEND_DIR = Path(__file__).resolve().parents[2]  # quickturf-backend/
_ALEMBIC_INI = _BACKEND_DIR / "alembic.ini"


def run_migrations() -> None:
    """Apply pending Alembic migrations against the configured database."""
    try:
        cfg = Config(str(_ALEMBIC_INI))
        cfg.set_main_option("script_location", str(_BACKEND_DIR / "alembic"))
        cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        command.upgrade(cfg, "head")
        logger.info("Database migrations up to date.")
    except Exception:  # pragma: no cover - defensive startup guard
        # Never block app startup on a migration failure (e.g. DB down).
        logger.exception("Failed to run database migrations on startup.")
