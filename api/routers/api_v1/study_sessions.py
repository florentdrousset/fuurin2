from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import StudySessions
from routers.api_v1.common import get_default_user_id

router = APIRouter(prefix="")


@router.get("/study-sessions", tags=["Study Sessions"]) 
def list_study_sessions(
    user_id: Optional[str] = None,
    work_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    uid = user_id or get_default_user_id(db)
    if not uid:
        return []

    q = select(
        StudySessions.id,
        StudySessions.started_at,
        StudySessions.ended_at,
        StudySessions.duration_sec,
        StudySessions.modality,
        StudySessions.work_id,
    ).where(StudySessions.user_id == uid)
    if work_id:
        q = q.where(StudySessions.work_id == work_id)
    q = q.order_by(StudySessions.started_at.desc()).limit(limit)
    rows = db.execute(q).all()
    return [
        {
            "id": str(r[0]),
            "started_at": r[1],
            "ended_at": r[2],
            "duration_sec": int(r[3] or 0),
            "modality": str(r[4]),
            "work_id": str(r[5]) if r[5] else None,
        }
        for r in rows
    ]
