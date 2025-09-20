"""initial schema

Revision ID: 202509201600
Revises: 
Create Date: 2025-09-20 16:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202509201600'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password_hash', sa.Text()),
        sa.Column('display_name', sa.Text()),
        sa.Column('avatar_url', sa.Text()),
        sa.Column('locale', sa.String()),
        sa.Column('timezone', sa.String()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True)),
    )

    # user_settings
    op.create_table(
        'user_settings',
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('daily_study_goal_minutes', sa.Integer()),
        sa.Column('weekly_study_goal_minutes', sa.Integer()),
        sa.Column('srs_prefs', sa.JSON()),
        sa.Column('notifications_prefs', sa.JSON()),
        sa.Column('premium_until', sa.DateTime(timezone=True)),
    )

    # works
    op.create_table(
        'works',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('author', sa.Text()),
        sa.Column('difficulty_level', sa.Integer()),
        sa.Column('source_url', sa.Text()),
        sa.Column('metadata', sa.JSON()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # work_segments
    op.create_table(
        'work_segments',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('works.id'), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('index_no', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text()),
        sa.Column('metadata', sa.JSON()),
    )
    op.create_index('ix_work_segments_work_id_index', 'work_segments', ['work_id', 'index_no'])

    # study_sessions
    op.create_table(
        'study_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_sec', sa.Integer(), nullable=False),
        sa.Column('modality', sa.String(), nullable=False),
        sa.Column('work_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('works.id')),
        sa.Column('work_segment_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('work_segments.id')),
        sa.Column('words_reviewed', sa.Integer()),
        sa.Column('words_learned', sa.Integer()),
        sa.Column('notes', sa.Text()),
    )
    op.create_index('ix_study_sessions_user_started', 'study_sessions', ['user_id', 'started_at'])

    # reading_speeds
    op.create_table(
        'reading_speeds',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('work_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('works.id'), nullable=False),
        sa.Column('measured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('chars_per_min', sa.Integer(), nullable=False),
        sa.Column('method', sa.String(), nullable=False),
    )

    # activity_events
    op.create_table(
        'activity_events',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('ref_kind', sa.String()),
        sa.Column('ref_id', postgresql.UUID(as_uuid=False)),
        sa.Column('summary', sa.Text()),
        sa.Column('metadata', sa.JSON()),
        sa.Column('visibility', sa.String(), nullable=False),
    )
    op.create_index('ix_activity_user_occurred', 'activity_events', ['user_id', 'occurred_at'])
    op.create_index('ix_activity_type_occurred', 'activity_events', ['type', 'occurred_at'])

    # achievements_catalog
    op.create_table(
        'achievements_catalog',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('code', sa.String(), nullable=False, unique=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.String()),
        sa.Column('criteria', sa.JSON()),
    )

    # user_achievements
    op.create_table(
        'user_achievements',
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('achievement_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('achievements_catalog.id'), primary_key=True),
        sa.Column('unlocked_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_new', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
    )
    op.create_index('ix_user_achievements_user_unlocked', 'user_achievements', ['user_id', 'unlocked_at'])

    # goals
    op.create_table(
        'goals',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('period', sa.String(), nullable=False),
        sa.Column('metric', sa.String(), nullable=False),
        sa.Column('target', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # goal_progress
    op.create_table(
        'goal_progress',
        sa.Column('goal_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('goals.id'), primary_key=True),
        sa.Column('measured_at', sa.DateTime(timezone=True), primary_key=True),
        sa.Column('value', sa.Integer(), nullable=False),
    )

    # notifications
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('read_at', sa.DateTime(timezone=True)),
    )

    # leaderboards
    op.create_table(
        'leaderboards',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column('scope', sa.String(), nullable=False),
        sa.Column('metric', sa.String(), nullable=False),
        sa.Column('period', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    # leaderboard_entries
    op.create_table(
        'leaderboard_entries',
        sa.Column('leaderboard_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('leaderboards.id'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('score', sa.Numeric(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('computed_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_leaderboard_entries_lb_rank', 'leaderboard_entries', ['leaderboard_id', 'rank'])


def downgrade() -> None:
    op.drop_index('ix_leaderboard_entries_lb_rank', table_name='leaderboard_entries')
    op.drop_table('leaderboard_entries')
    op.drop_table('leaderboards')
    op.drop_table('notifications')
    op.drop_table('goal_progress')
    op.drop_table('goals')
    op.drop_index('ix_user_achievements_user_unlocked', table_name='user_achievements')
    op.drop_table('user_achievements')
    op.drop_table('achievements_catalog')
    op.drop_index('ix_activity_type_occurred', table_name='activity_events')
    op.drop_index('ix_activity_user_occurred', table_name='activity_events')
    op.drop_table('activity_events')
    op.drop_table('reading_speeds')
    op.drop_index('ix_study_sessions_user_started', table_name='study_sessions')
    op.drop_table('study_sessions')
    op.drop_index('ix_work_segments_work_id_index', table_name='work_segments')
    op.drop_table('work_segments')
    op.drop_table('works')
    op.drop_table('user_settings')
    op.drop_table('users')
