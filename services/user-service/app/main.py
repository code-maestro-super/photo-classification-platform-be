from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.routers import auth
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="User authentication and management service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}


@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.app_name} starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{settings.app_name} shutting down...")

