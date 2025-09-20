from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from db.database import SessionLocal
from db.models import (
    Users,
    UserSettings,
    Works,
    StudySessions,
    ActivityEvents,
    ReadingSpeeds,
    Modality,
    ActivityType,
)


def ensure_seed(session: Session) -> None:
    # If a user already exists, do nothing
    existing = session.execute(select(Users.id).limit(1)).first()
    if existing:
        return

    now = datetime.now(timezone.utc)

    # Create user
    user_id = str(uuid.uuid4())
    user = Users(
        id=user_id,
        email="test@example.com",
        display_name="Test User",
        timezone="Europe/Paris",
        created_at=now,
        updated_at=now,
    )
    session.add(user)

    settings = UserSettings(
        user_id=user_id,
        daily_study_goal_minutes=20,
        weekly_study_goal_minutes=120,
    )
    session.add(settings)

    # Works
    work1_id = str(uuid.uuid4())
    work2_id = str(uuid.uuid4())
    w1 = Works(id=work1_id, title="Spy x Family", type="manga", created_at=now, updated_at=now)
    w2 = Works(id=work2_id, title="Amakano 2", type="game", created_at=now, updated_at=now)
    session.add_all([w1, w2])

    # Study sessions over the past 10 days
    sessions = []
    for i, minutes in enumerate([45, 32, 67, 23, 89, 56, 34, 12, 23, 15]):
        start = now - timedelta(days=9 - i, hours=2)
        end = start + timedelta(minutes=minutes)
        s = StudySessions(
            id=str(uuid.uuid4()),
            user_id=user_id,
            started_at=start,
            ended_at=end,
            duration_sec=int((end - start).total_seconds()),
            modality=Modality.read.value,
            work_id=work1_id if i % 2 == 0 else work2_id,
            words_learned=0,
            words_reviewed=None,
            notes=None,
        )
        sessions.append(s)
    session.add_all(sessions)

    # Activity events
    events = []
    samples = [
        ("Spent 15 minutes on 'Amakano 2'", work2_id),
        ("Spent 12 minutes on 'Amakano 2'", work2_id),
        ("Spent 23 minutes on 'Amakano 2'", work2_id),
        ("Read 32 pages of 'Spy x Family'", work1_id),
        ("Completed vocabulary review", None),
    ]
    for i, (summary, wid) in enumerate(samples):
        ev = ActivityEvents(
            id=str(uuid.uuid4()),
            user_id=user_id,
            occurred_at=now - timedelta(days=i+1),
            type=ActivityType.session_logged.value,
            ref_kind='work' if wid else None,
            ref_id=wid,
            summary=summary,
            visibility='private',
        )
        events.append(ev)
    session.add_all(events)

    # Reading speeds
    speeds = []
    for i, cpm in enumerate([120, 140, 160, 150]):
        speeds.append(ReadingSpeeds(
            id=str(uuid.uuid4()), user_id=user_id, work_id=work1_id,
            measured_at=now - timedelta(days=20 - i*2), chars_per_min=cpm, method='manual'
        ))
    session.add_all(speeds)

    # Commit all
    session.commit()


def main():
    db = SessionLocal()
    try:
        ensure_seed(db)
        print("Seed completed")
    finally:
        db.close()


if __name__ == "__main__":
    main()
