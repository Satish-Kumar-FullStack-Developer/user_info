"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_routes import router as user_router
from services.db import connect_db, close_db_connection
from config import settings
import logging

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Register routers
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    """Initialize application on startup."""
    logger.info("Starting application...")
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    """Clean up on shutdown."""
    logger.info("Shutting down application...")
    await close_db_connection()


@app.get("/", tags=["health"])
async def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "Service is running"}


@app.get("/api/health", tags=["health"])
async def api_health():
    """API health check with database connection status."""
    try:
        from services.db import db
        await db.command("ping")
        logger.info("Health check passed")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

