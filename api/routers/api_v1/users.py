from __future__ import annotations

from datetime import datetime, timedelta, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import Users, StudySessions
from routers.api_v1.common import minutes
from schemas.summary import MeSummary

router = APIRouter(prefix="")


@router.get("/users", tags=["Users"]) 
def list_users(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    rows = db.execute(
        select(Users.id, Users.display_name, Users.email).order_by(Users.created_at.asc()).limit(limit)
    ).all()
    return [{"id": str(r[0]), "display_name": r[1], "email": r[2]} for r in rows]


@router.get("/users/{user_id}", tags=["Users"]) 
def get_user(user_id: str, db: Session = Depends(get_db)):
    row = db.execute(select(Users.id, Users.display_name, Users.email, Users.timezone).where(Users.id == user_id)).first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(row[0]), "display_name": row[1], "email": row[2], "timezone": row[3]}


@router.get("/users/{user_id}/summary", response_model=MeSummary, tags=["Users"]) 
def user_summary(user_id: str, db: Session = Depends(get_db)):
    total_words = db.execute(
        select(func.coalesce(func.sum(StudySessions.words_learned), 0)).where(StudySessions.user_id == user_id)
    ).scalar_one()

    since = datetime.utcnow() - timedelta(days=7)
    total_sec_7d = db.execute(
        select(func.coalesce(func.sum(StudySessions.duration_sec), 0)).where(
            (StudySessions.user_id == user_id) & (StudySessions.started_at >= since)
        )
    ).scalar_one()

    rows = db.execute(
        select(func.date_trunc('day', StudySessions.started_at)).where(StudySessions.user_id == user_id)
    ).all()
    days = {r[0].date() for r in rows if r and r[0] is not None}
    streak = 0
    cur = date.today()
    while cur in days:
        streak += 1
        cur = cur - timedelta(days=1)

    return MeSummary(
        total_words_learned=int(total_words or 0),
        study_time_minutes_7d=minutes(int(total_sec_7d or 0)),
        streak_days=streak,
    )
