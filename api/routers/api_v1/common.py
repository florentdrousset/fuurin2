from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Users


def get_default_user_id(db: Session) -> Optional[str]:
    row = db.execute(select(Users.id).order_by(Users.created_at.asc())).first()
    return row[0] if row else None


def minutes(seconds: Optional[int]) -> int:
    if not seconds:
        return 0
    return int(seconds // 60)
