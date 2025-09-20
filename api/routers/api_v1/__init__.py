from __future__ import annotations

from fastapi import APIRouter

from .health import router as health_router
from .users import router as users_router
from .works import router as works_router
from .study_sessions import router as study_sessions_router
from .activity_events import router as activity_events_router
from .stats import router as stats_router

router = APIRouter()

# Compose all entity routers under one v1 router
router.include_router(health_router)
router.include_router(users_router)
router.include_router(works_router)
router.include_router(study_sessions_router)
router.include_router(activity_events_router)
router.include_router(stats_router)
