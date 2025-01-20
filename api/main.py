from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from . import models, database
from .routers import campaigns, events

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
try:
    models.Base.metadata.create_all(bind=database.engine)
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(campaigns.router)
app.include_router(events.router)
