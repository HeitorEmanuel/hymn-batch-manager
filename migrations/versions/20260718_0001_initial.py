"""Cria o esquema inicial completo.

Revision ID: 20260718_0001
Revises:
"""
from __future__ import annotations

from alembic import op

from app.database.base import Base
from app.database import models  # noqa: F401

revision = "20260718_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())

