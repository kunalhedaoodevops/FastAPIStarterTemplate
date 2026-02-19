"""alter filestore table for the owner id

Revision ID: ac471dbbaba4
Revises: baabfe25d334
Create Date: 2026-02-19 20:49:28.116414
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ac471dbbaba4'
down_revision: Union[str, Sequence[str], None] = 'baabfe25d334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("filestore") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_filestore_owner_id_users",
            "users",   # change to "users" if needed
            ["owner_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("filestore") as batch_op:
        batch_op.drop_constraint("fk_filestore_owner_id_users", type_="foreignkey")
        batch_op.drop_column("owner_id")
