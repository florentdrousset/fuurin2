from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import StudySessions
from routers.api_v1.common import get_default_user_id, minutes

router = APIRouter(prefix="")


@router.get("/stats/daily", tags=["Stats"]) 
def stats_daily(
    user_id: Optional[str] = None,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    uid = user_id or get_default_user_id(db)
    if not uid:
        return {"minutes_by_date": {}, "words_by_date": {}}

    if not end:
        end = date.today() + timedelta(days=1)
    if not start:
        start = end - timedelta(days=365)

    rows = db.execute(
        select(
            func.date_trunc('day', StudySessions.started_at).label('d'),
            func.sum(StudySessions.duration_sec).label('sec'),
            func.sum(func.coalesce(StudySessions.words_learned, 0)).label('words'),
        )
        .where(
            (StudySessions.user_id == uid)
            & (StudySessions.started_at >= start)
            & (StudySessions.started_at < end)
        )
        .group_by('d')
    ).all()

    minutes_by_date = {r[0].date().isoformat(): minutes(int(r[1] or 0)) for r in rows}
    words_by_date = {r[0].date().isoformat(): int(r[2] or 0) for r in rows}
    return {"minutes_by_date": minutes_by_date, "words_by_date": words_by_date}


@router.get("/stats/weekly", tags=["Stats"]) 
def stats_weekly(
    user_id: Optional[str] = None,
    week: Optional[str] = Query(None, pattern=r"^\d{4}-W\d{2}$"),
    db: Session = Depends(get_db),
):
    if not week:
        today = date.today()
        iso_year, iso_week, _ = today.isocalendar()
        week = f"{iso_year}-W{iso_week:02d}"
    year = int(week[:4])
    wnum = int(week[-2:])
    jan4 = date(year, 1, 4)
    jan4_monday = jan4 - timedelta(days=jan4.isoweekday() - 1)
    week_start = jan4_monday + timedelta(weeks=wnum - 1)
    week_end = week_start + timedelta(days=7)

    uid = user_id or get_default_user_id(db)
    if not uid:
        return {"week": week, "minutes": [0] * 7}

    rows = db.execute(
        select(
            func.date_trunc('day', StudySessions.started_at).label('d'),
            func.sum(StudySessions.duration_sec).label('sec')
        )
        .where((StudySessions.user_id == uid) & (StudySessions.started_at >= week_start) & (StudySessions.started_at < week_end))
        .group_by('d')
    ).all()

    by_day = {r[0].date(): minutes(int(r[1] or 0)) for r in rows}
    minutes_series = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        minutes_series.append(by_day.get(d, 0))
    return {"week": week, "minutes": minutes_series}
