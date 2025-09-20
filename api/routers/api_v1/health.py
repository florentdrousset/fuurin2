from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"]) 
def health_v1():
    return {"status": "ok", "api": "v1"}
