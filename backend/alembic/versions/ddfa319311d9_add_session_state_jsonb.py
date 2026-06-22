"""add_session_state_jsonb

Revision ID: ddfa319311d9
Revises: d91f126e865a
Create Date: 2026-06-19 03:44:33.444327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = 'ddfa319311d9'
down_revision: Union[str, None] = 'd91f126e865a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'interview_sessions',
        sa.Column('session_state', JSONB, nullable=True)
    )
    op.create_index(
        op.f('ix_interview_sessions_user_id'),
        'interview_sessions',
        ['user_id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_interview_sessions_user_id'), table_name='interview_sessions')
    op.drop_column('interview_sessions', 'session_state')