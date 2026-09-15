"""Preserve audit rows when complaints are deleted.

Revision ID: 0002_preserve_audit_history
Revises: 0001_initial_schema
Create Date: 2026-09-15
"""
from typing import Sequence, Union

from alembic import op


revision: str = "0002_preserve_audit_history"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "audit_logs_complaint_id_fkey",
        "audit_logs",
        type_="foreignkey",
    )


def downgrade() -> None:
    op.create_foreign_key(
        "audit_logs_complaint_id_fkey",
        "audit_logs",
        "complaints",
        ["complaint_id"],
        ["id"],
        ondelete="CASCADE",
    )
