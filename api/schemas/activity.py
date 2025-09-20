from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WorkMini(BaseModel):
    id: str
    title: str
    type: str


class ActivityItem(BaseModel):
    id: str
    occurred_at: datetime
    type: str
    summary: str
    work: Optional[WorkMini] = None
