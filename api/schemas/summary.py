from __future__ import annotations

from pydantic import BaseModel


class MeSummary(BaseModel):
    total_words_learned: int
    study_time_minutes_7d: int
    streak_days: int
