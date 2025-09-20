from __future__ import annotations

from datetime import datetime, timedelta, date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import (
    Users,
    StudySessions,
    ActivityEvents,
    Works,
    ReadingSpeeds,
)
from schemas.summary import MeSummary
from schemas.activity import ActivityItem, WorkMini

router = APIRouter()


# Helpers

def _get_default_user_id(db: Session) -> Optional[str]:
    row = db.execute(select(Users.id).order_by(Users.created_at.asc())).first()
    return row[0] if row else None


def _minutes(seconds: Optional[int]) -> int:
    if not seconds:
        return 0
    return int(seconds // 60)


@router.get("/health", tags=["Health"]) 
def health_v1():
    return {"status": "ok", "api": "v1"}


@router.get("/me/summary", response_model=MeSummary, tags=["Me (deprecated)"])
def me_summary(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    # Pick default user if not provided (no auth yet)
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return MeSummary(total_words_learned=0, study_time_minutes_7d=0, streak_days=0)

    # total_words_learned: sum words_learned
    total_words = db.execute(
        select(func.coalesce(func.sum(StudySessions.words_learned), 0)).where(StudySessions.user_id == uid)
    ).scalar_one()

    # study_time_minutes_7d: last 7 days total
    since = datetime.utcnow() - timedelta(days=7)
    total_sec_7d = db.execute(
        select(func.coalesce(func.sum(StudySessions.duration_sec), 0)).where(
            (StudySessions.user_id == uid) & (StudySessions.started_at >= since)
        )
    ).scalar_one()

    # streak_days: count of consecutive days with any study from today backward
    # Compute set of dates with activity
    rows = db.execute(
        select(func.date_trunc('day', StudySessions.started_at)).where(StudySessions.user_id == uid)
    ).all()
    days = {r[0].date() for r in rows if r and r[0] is not None}
    streak = 0
    cur = date.today()
    while cur in days:
        streak += 1
        cur = cur - timedelta(days=1)

    return MeSummary(
        total_words_learned=int(total_words or 0),
        study_time_minutes_7d=_minutes(int(total_sec_7d or 0)),
        streak_days=streak,
    )


@router.get("/me/activity", response_model=list[ActivityItem], tags=["Me (deprecated)"])
def me_activity(
    limit: int = Query(50, ge=1, le=200),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return []

    # Fetch activity events with possible work join when ref_kind == 'work'
    events = db.execute(
        select(
            ActivityEvents.id,
            ActivityEvents.occurred_at,
            ActivityEvents.type,
            ActivityEvents.summary,
            ActivityEvents.ref_kind,
            ActivityEvents.ref_id,
            Works.id,
            Works.title,
            Works.type,
        )
        .select_from(ActivityEvents)
        .outerjoin(Works, (ActivityEvents.ref_kind == 'work') & (ActivityEvents.ref_id == Works.id))
        .where(ActivityEvents.user_id == uid)
        .order_by(ActivityEvents.occurred_at.desc())
        .limit(limit)
    ).all()

    items: list[ActivityItem] = []
    for e in events:
        work = None
        if e[6] is not None:
            work = WorkMini(id=str(e[6]), title=e[7] or "", type=str(e[8]))
        items.append(
            ActivityItem(
                id=str(e[0]),
                occurred_at=e[1],
                type=str(e[2]),
                summary=e[3] or "",
                work=work,
            )
        )
    return items


@router.get("/me/heatmap", tags=["Me (deprecated)"])
def me_heatmap(year: int = Query(..., ge=2000, le=2100), user_id: Optional[str] = None, db: Session = Depends(get_db)):
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return {}

    start = date(year, 1, 1)
    end = date(year + 1, 1, 1)

    rows = db.execute(
        select(func.date_trunc('day', StudySessions.started_at).label('d'), func.sum(StudySessions.duration_sec).label('sec'))
        .where((StudySessions.user_id == uid) & (StudySessions.started_at >= start) & (StudySessions.started_at < end))
        .group_by('d')
    ).all()

    return {r[0].date().isoformat(): _minutes(int(r[1] or 0)) for r in rows}


@router.get("/me/weekly-study", tags=["Me (deprecated)"])
def weekly_study(week: str = Query(None, pattern=r"^\d{4}-W\d{2}$"), user_id: Optional[str] = None, db: Session = Depends(get_db)):
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return {"week": week, "minutes": [0, 0, 0, 0, 0, 0, 0]}

    # Determine ISO week range
    if not week:
        today = date.today()
        iso_year, iso_week, _ = today.isocalendar()
        week = f"{iso_year}-W{iso_week:02d}"
    year = int(week[:4])
    wnum = int(week[-2:])
    # ISO week: Monday is 1
    # Find Monday of the ISO week
    # Start with Jan 4th (always in week 1), then compute
    jan4 = date(year, 1, 4)
    jan4_monday = jan4 - timedelta(days=jan4.isoweekday() - 1)
    week_start = jan4_monday + timedelta(weeks=wnum - 1)
    week_end = week_start + timedelta(days=7)

    rows = db.execute(
        select(func.date_trunc('day', StudySessions.started_at).label('d'), func.sum(StudySessions.duration_sec).label('sec'))
        .where((StudySessions.user_id == uid) & (StudySessions.started_at >= week_start) & (StudySessions.started_at < week_end))
        .group_by('d')
    ).all()
    by_day = {r[0].date(): _minutes(int(r[1] or 0)) for r in rows}
    minutes = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        minutes.append(by_day.get(d, 0))

    return {"week": week, "minutes": minutes}


@router.get("/works", tags=["Works"])
def list_works(db: Session = Depends(get_db)):
    rows = db.execute(select(Works.id, Works.title, Works.type).order_by(Works.created_at.desc())).all()
    return [{"id": str(r[0]), "title": r[1], "type": str(r[2])} for r in rows]


@router.get("/reading-speeds", tags=["Reading Speeds"])
def reading_speeds(work_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = select(ReadingSpeeds.work_id, Works.title, func.array_agg(ReadingSpeeds.chars_per_min).label('cpm')) \
        .join(Works, Works.id == ReadingSpeeds.work_id) \
        .group_by(ReadingSpeeds.work_id, Works.title)

    if work_id:
        q = q.where(ReadingSpeeds.work_id == work_id)

    rows = db.execute(q).all()
    series = []
    for r in rows:
        series.append({
            "work": {"id": str(r[0]), "title": r[1]},
            "cpm": list(r[2]) if r[2] is not None else [],
        })
    return {"series": series}


# ==== Entity-centric endpoints (added) ====

from fastapi import HTTPException
from sqlalchemy import and_, cast, Date


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
    # total_words_learned
    total_words = db.execute(
        select(func.coalesce(func.sum(StudySessions.words_learned), 0)).where(StudySessions.user_id == user_id)
    ).scalar_one()

    # last 7 days study time
    since = datetime.utcnow() - timedelta(days=7)
    total_sec_7d = db.execute(
        select(func.coalesce(func.sum(StudySessions.duration_sec), 0)).where(
            (StudySessions.user_id == user_id) & (StudySessions.started_at >= since)
        )
    ).scalar_one()

    # streak days
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
        study_time_minutes_7d=_minutes(int(total_sec_7d or 0)),
        streak_days=streak,
    )


@router.get("/activity-events", tags=["Activity Events"])
def list_activity_events(
    user_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return []

    events = db.execute(
        select(
            ActivityEvents.id,
            ActivityEvents.occurred_at,
            ActivityEvents.type,
            ActivityEvents.summary,
            ActivityEvents.ref_kind,
            ActivityEvents.ref_id,
            Works.id,
            Works.title,
            Works.type,
        )
        .select_from(ActivityEvents)
        .outerjoin(Works, (ActivityEvents.ref_kind == 'work') & (ActivityEvents.ref_id == Works.id))
        .where(ActivityEvents.user_id == uid)
        .order_by(ActivityEvents.occurred_at.desc())
        .limit(limit)
    ).all()

    items: list[ActivityItem] = []
    for e in events:
        work = None
        if e[6] is not None:
            work = WorkMini(id=str(e[6]), title=e[7] or "", type=str(e[8]))
        items.append(
            ActivityItem(
                id=str(e[0]),
                occurred_at=e[1],
                type=str(e[2]),
                summary=e[3] or "",
                work=work,
            )
        )
    return items


@router.get("/stats/daily", tags=["Stats"])
def stats_daily(
    user_id: Optional[str] = None,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return {"minutes_by_date": {}, "words_by_date": {}}

    # Default to last 365 days if no range
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

    minutes_by_date = {r[0].date().isoformat(): _minutes(int(r[1] or 0)) for r in rows}
    words_by_date = {r[0].date().isoformat(): int(r[2] or 0) for r in rows}
    return {"minutes_by_date": minutes_by_date, "words_by_date": words_by_date}


@router.get("/stats/weekly", tags=["Stats"])
def stats_weekly(
    user_id: Optional[str] = None,
    week: Optional[str] = Query(None, pattern=r"^\d{4}-W\d{2}$"),
    db: Session = Depends(get_db),
):
    # Reuse weekly range computation from the previous handler
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

    uid = user_id or _get_default_user_id(db)
    if not uid:
        return {"week": week, "minutes": [0]*7}

    rows = db.execute(
        select(
            func.date_trunc('day', StudySessions.started_at).label('d'),
            func.sum(StudySessions.duration_sec).label('sec')
        )
        .where((StudySessions.user_id == uid) & (StudySessions.started_at >= week_start) & (StudySessions.started_at < week_end))
        .group_by('d')
    ).all()

    by_day = {r[0].date(): _minutes(int(r[1] or 0)) for r in rows}
    minutes = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        minutes.append(by_day.get(d, 0))
    return {"week": week, "minutes": minutes}


@router.get("/study-sessions", tags=["Study Sessions"])
def list_study_sessions(
    user_id: Optional[str] = None,
    work_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    uid = user_id or _get_default_user_id(db)
    if not uid:
        return []
    q = select(
        StudySessions.id,
        StudySessions.started_at,
        StudySessions.ended_at,
        StudySessions.duration_sec,
        StudySessions.modality,
        StudySessions.work_id
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
