from __future__ import annotations

import enum
from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    Date,
    ForeignKey,
    Boolean,
    JSON,
    UniqueConstraint,
    Index,
    Numeric,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()


class WorkType(str, enum.Enum):
    book = "book"
    manga = "manga"
    anime = "anime"
    game = "game"
    other = "other"


class SegmentKind(str, enum.Enum):
    chapter = "chapter"
    episode = "episode"
    page_range = "page_range"
    scene = "scene"
    other = "other"


class Modality(str, enum.Enum):
    practice = "practice"
    listen = "listen"
    write = "write"
    speak = "speak"
    review = "review"
    read = "read"


class ActivityType(str, enum.Enum):
    session_logged = "session_logged"
    review_completed = "review_completed"
    achievement_unlocked = "achievement_unlocked"
    goal_reached = "goal_reached"
    media_added = "media_added"
    vocabulary_mastered = "vocabulary_mastered"
    streak_extended = "streak_extended"


class Visibility(str, enum.Enum):
    private = "private"
    friends = "friends"
    public = "public"


class GoalPeriod(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class GoalMetric(str, enum.Enum):
    words_learned = "words_learned"
    study_minutes = "study_minutes"


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    past_due = "past_due"
    canceled = "canceled"
    trialing = "trialing"


class ReadingSpeedMethod(str, enum.Enum):
    manual = "manual"
    auto = "auto"


class LeaderboardScope(str, enum.Enum):
    global_ = "global"
    friends = "friends"
    local = "local"


class LeaderboardMetric(str, enum.Enum):
    study_minutes = "study_minutes"
    words_learned = "words_learned"
    streak_days = "streak_days"


class LeaderboardPeriod(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    all_time = "all_time"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    display_name: Mapped[Optional[str]] = mapped_column(Text)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    locale: Mapped[Optional[str]] = mapped_column(String)
    timezone: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    settings: Mapped["UserSettings"] = relationship("UserSettings", back_populates="user", uselist=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), primary_key=True)
    daily_study_goal_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    weekly_study_goal_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    srs_prefs: Mapped[Optional[dict]] = mapped_column(JSON)
    notifications_prefs: Mapped[Optional[dict]] = mapped_column(JSON)
    premium_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped[Users] = relationship("Users", back_populates="settings")


class Works(Base):
    __tablename__ = "works"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[WorkType] = mapped_column(String, nullable=False)
    author: Mapped[Optional[str]] = mapped_column(Text)
    difficulty_level: Mapped[Optional[int]] = mapped_column(Integer)
    source_url: Mapped[Optional[str]] = mapped_column(Text)
    meta: Mapped[Optional[dict]] = mapped_column("metadata", JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class WorkSegments(Base):
    __tablename__ = "work_segments"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    work_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("works.id"), nullable=False)
    kind: Mapped[SegmentKind] = mapped_column(String, nullable=False)
    index_no: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    meta: Mapped[Optional[dict]] = mapped_column("metadata", JSON)

    work: Mapped[Works] = relationship("Works", backref="segments")

    __table_args__ = (
        Index("ix_work_segments_work_id_index", "work_id", "index_no"),
    )


class StudySessions(Base):
    __tablename__ = "study_sessions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    modality: Mapped[Modality] = mapped_column(String, nullable=False)
    work_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("works.id"))
    work_segment_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("work_segments.id"))
    words_reviewed: Mapped[Optional[int]] = mapped_column(Integer)
    words_learned: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    __table_args__ = (
        Index("ix_study_sessions_user_started", "user_id", "started_at"),
    )


class ReadingSpeeds(Base):
    __tablename__ = "reading_speeds"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    work_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("works.id"), nullable=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    chars_per_min: Mapped[int] = mapped_column(Integer, nullable=False)
    method: Mapped[ReadingSpeedMethod] = mapped_column(String, nullable=False)


class ActivityEvents(Base):
    __tablename__ = "activity_events"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    type: Mapped[ActivityType] = mapped_column(String, nullable=False)
    ref_kind: Mapped[Optional[str]] = mapped_column(String)
    ref_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    meta: Mapped[Optional[dict]] = mapped_column("metadata", JSON)
    visibility: Mapped[Visibility] = mapped_column(String, nullable=False, default=Visibility.private.value)

    __table_args__ = (
        Index("ix_activity_user_occurred", "user_id", "occurred_at"),
        Index("ix_activity_type_occurred", "type", "occurred_at"),
    )


class AchievementsCatalog(Base):
    __tablename__ = "achievements_catalog"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    icon: Mapped[Optional[str]] = mapped_column(String)
    criteria: Mapped[Optional[dict]] = mapped_column(JSON)


class UserAchievements(Base):
    __tablename__ = "user_achievements"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), primary_key=True)
    achievement_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("achievements_catalog.id"), primary_key=True)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_new: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        Index("ix_user_achievements_user_unlocked", "user_id", "unlocked_at"),
    )


class Goals(Base):
    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    period: Mapped[GoalPeriod] = mapped_column(String, nullable=False)
    metric: Mapped[GoalMetric] = mapped_column(String, nullable=False)
    target: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class GoalProgress(Base):
    __tablename__ = "goal_progress"

    goal_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("goals.id"), primary_key=True)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class Notifications(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class Leaderboards(Base):
    __tablename__ = "leaderboards"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    scope: Mapped[LeaderboardScope] = mapped_column(String, nullable=False)
    metric: Mapped[LeaderboardMetric] = mapped_column(String, nullable=False)
    period: Mapped[LeaderboardPeriod] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class LeaderboardEntries(Base):
    __tablename__ = "leaderboard_entries"

    leaderboard_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("leaderboards.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), primary_key=True)
    score: Mapped[float] = mapped_column(Numeric, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_leaderboard_entries_lb_rank", "leaderboard_id", "rank"),
    )
