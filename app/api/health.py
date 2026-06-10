# app/api/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis

from app.db.session import get_db
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health-check")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint validating core infrastructure connections."""
    db_status = "healthy"
    redis_status = "healthy"
    gemini_config_status = "configured" if settings.GEMINI_API_KEY else "missing"

    # Verify SQL database connection
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Health check database failure: {e}")
        db_status = f"unhealthy: {str(e)}"

    # Verify Redis cache connection
    if settings.REDIS_HOST not in ("redis", ""):
        try:
            r = aioredis.from_url(settings.REDIS_URL)
            await r.ping()
            await r.close()
        except Exception as e:
            logger.error("Health check Redis failure", error=str(e))
            redis_status = f"unhealthy: {str(e)}"
    else:
        redis_status = "skipped (POC mode)"

    overall_status = "healthy"
    if "unhealthy" in db_status or "unhealthy" in redis_status: 
        overall_status = "unhealthy"

    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status,
        "gemini_api": gemini_config_status,
    }
