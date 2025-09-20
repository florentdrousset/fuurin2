from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import ActivityEvents, Works
from routers.api_v1.common import get_default_user_id
from schemas.activity import ActivityItem, WorkMini

router = APIRouter(prefix="")


@router.get("/activity-events", tags=["Activity Events"], response_model=list[ActivityItem]) 
def list_activity_events(
    user_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    uid = user_id or get_default_user_id(db)
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
