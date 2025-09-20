from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import Works, ReadingSpeeds

router = APIRouter(prefix="")


@router.get("/works", tags=["Works"]) 
def list_works(db: Session = Depends(get_db)):
    rows = db.execute(select(Works.id, Works.title, Works.type).order_by(Works.created_at.desc())).all()
    return [{"id": str(r[0]), "title": r[1], "type": str(r[2])} for r in rows]


@router.get("/reading-speeds", tags=["Reading Speeds"]) 
def reading_speeds(work_id: Optional[str] = None, db: Session = Depends(get_db)):
    q = (
        select(ReadingSpeeds.work_id, Works.title, func.array_agg(ReadingSpeeds.chars_per_min).label('cpm'))
        .join(Works, Works.id == ReadingSpeeds.work_id)
        .group_by(ReadingSpeeds.work_id, Works.title)
    )
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
