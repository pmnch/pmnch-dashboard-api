from fastapi import APIRouter

from app.api.v1.endpoints.campaigns import router as campaigns_router
from app.api.v1.endpoints.health_check import router as health_check_router
from app.api.v1.endpoints.info import router as info_router

api_router = APIRouter()
api_router.include_router(campaigns_router, tags=["Campaigns"])
api_router.include_router(health_check_router, tags=["Health Check"])
api_router.include_router(info_router, tags=["Info"])