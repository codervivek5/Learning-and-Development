# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Application configuration
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.database import init_db

# ============================================================
# Middleware Imports
# ============================================================

from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.auth_middleware import AuthMiddleware

# ============================================================
# API Router Imports
# ============================================================

from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.uploads import router as uploads_router
from app.api.analysis import router as analysis_router
from app.api.ai import router as ai_router
from app.api.design import router as design_router
from app.api.development import router as development_router
from app.api.review import router as review_router
from app.api.provider import router as provider_router
from app.api.export import router as export_router
from app.api.workflow import router as workflow_router
from app.api.health import router as health_router
from app.api.dashboard import router as dashboard_router
from app.api.admin import router as admin_router

# ============================================================
# WebSocket Router
# ============================================================

from app.websocket.ws_handler import router as ws_router

# ============================================================
# Logging Configuration
# ============================================================

setup_logging()
logger = get_logger(__name__)


# ============================================================
# Application Lifecycle Events
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executes during application startup and shutdown.

    Startup:
        - Initialize database
        - Create tables if required

    Shutdown:
        - Perform cleanup tasks
    """

    logger.info("Starting FastAPI application")

    try:
        await init_db()
        logger.info("Database tables initialized successfully")

    except Exception as e:
        logger.exception(
            "Failed to initialize database tables",
            error=str(e)
        )

    yield

    logger.info("Shutting down FastAPI application")


# ============================================================
# FastAPI Application Instance
# ============================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)


# ============================================================
# CORS Configuration
# ============================================================

if settings.BACKEND_CORS_ORIGINS:

    allow_origins = [
        str(origin)
        for origin in settings.BACKEND_CORS_ORIGINS
    ]

    # Replace wildcard with explicit development origins
    if "*" in allow_origins:
        allow_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ============================================================
# Global Middleware Registration
# ============================================================

# Request/Response logging middleware
app.add_middleware(LoggingMiddleware)

# JWT/API authentication middleware
app.add_middleware(AuthMiddleware)


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root health endpoint.

    Returns basic API information.
    """

    return {
        "status": "success",
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs_url": "/docs",
        "openapi_url": f"{settings.API_V1_STR}/openapi.json",
    }


# ============================================================
# Router Registration
# ============================================================

# Admin Management APIs
app.include_router(
    admin_router,
    prefix=f"{settings.API_V1_STR}",
    tags=["Admin"],
)

# Authentication APIs
app.include_router(
    auth_router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"],
)

# Project Management APIs
app.include_router(
    projects_router,
    prefix=f"{settings.API_V1_STR}/projects",
    tags=["Projects"],
)

# Dashboard APIs
app.include_router(
    dashboard_router,
    prefix=f"{settings.API_V1_STR}/dashboard",
    tags=["Dashboard"],
)

# File Upload APIs
app.include_router(
    uploads_router,
    prefix=f"{settings.API_V1_STR}/uploads",
    tags=["Uploads"],
)

# Analysis APIs
app.include_router(
    analysis_router,
    prefix=f"{settings.API_V1_STR}/analysis",
    tags=["Analysis"],
)

# AI Processing APIs
app.include_router(
    ai_router,
    prefix=f"{settings.API_V1_STR}/ai",
    tags=["AI"],
)

# Design Generation APIs
app.include_router(
    design_router,
    prefix=f"{settings.API_V1_STR}/design",
    tags=["Design"],
)

# Development APIs
app.include_router(
    development_router,
    prefix=f"{settings.API_V1_STR}/development",
    tags=["Development"],
)

# Review APIs
app.include_router(
    review_router,
    prefix=f"{settings.API_V1_STR}/review",
    tags=["Review"],
)

# Provider Configuration APIs
app.include_router(
    provider_router,
    prefix=f"{settings.API_V1_STR}",
    tags=["Provider"],
)

# Export APIs
app.include_router(
    export_router,
    prefix=f"{settings.API_V1_STR}/export",
    tags=["Export"],
)

# Workflow APIs
app.include_router(
    workflow_router,
    prefix=f"{settings.API_V1_STR}/workflow",
    tags=["Workflow"],
)

# Health Check APIs
app.include_router(
    health_router,
    prefix=f"{settings.API_V1_STR}/health",
    tags=["Health"],
)

# ============================================================
# WebSocket Routes
# ============================================================

app.include_router(
    ws_router,
    tags=["WebSockets"],
)