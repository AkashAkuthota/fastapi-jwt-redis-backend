from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks.token_cleanup import cleanup_tokens
from app.db.database import engine
import app.db.database_models as database_models

from app.routers.auth_router import router as auth_router
from app.routers.product_router import router as product_router
from app.routers.cart_router import router as cart_router

import logging

import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create tables
    database_models.Base.metadata.create_all(bind=engine)

    # Scheduler
    scheduler = BackgroundScheduler(daemon=True)

    scheduler.add_job(
        cleanup_tokens,
        "interval",
        minutes=10
    )

    scheduler.start()

    yield

    scheduler.shutdown()



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)


app = FastAPI(
    title="Product Inventory Backend API",
    description="Secure FastAPI backend with JWT authentication, refresh token rotation, Redis blacklist, RBAC, rate limiting, and scheduled token cleanup.",
    version="1.0.0",
    lifespan=lifespan
)

#add root health endpoint
@app.get("/")
def root():
    return {"message": "FastAPI Product Inventory API is running"}




# CORS configuration

FRONTEND_URL = os.getenv("FRONTEND_URL", "")

origins = ["http://localhost:5173"]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)
