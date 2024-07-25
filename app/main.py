import logging
import logging.config
from datetime import datetime, timedelta
from fastapi import FastAPI
from starlette.responses import JSONResponse
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
import os

# Determine the base directory (the parent directory of the app folder)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the logging configuration file
logging_conf_path = os.path.join(base_dir, 'logging.conf')

# Load logging configuration
logging.config.fileConfig(logging_conf_path)

# Create the logger
logger = logging.getLogger('app')

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)
    logger.info("Application startup: Database initialized")

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logger.error("An unexpected error occurred", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

app.include_router(user_routes.router)
