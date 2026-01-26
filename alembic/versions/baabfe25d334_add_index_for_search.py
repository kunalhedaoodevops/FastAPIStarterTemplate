"""add index for search

Revision ID: baabfe25d334
Revises: 95b0c300827d
Create Date: 2025-12-21 12:32:25.505257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baabfe25d334'
down_revision: Union[str, Sequence[str], None] = '95b0c300827d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Items table
    op.create_index("idx_items_title", "items", ["title"])
    op.create_index("idx_items_description", "items", ["description"])
    op.create_index("idx_items_price", "items", ["price"])
    op.create_index("idx_items_owner_id", "items", ["owner_id"])
    op.create_index("idx_items_id", "items", ["id"])

    # Users table
    op.create_index("idx_users_email", "users", ["email"], unique=True)
    op.create_index("idx_users_full_name", "users", ["full_name"])
    op.create_index("idx_users_role", "users", ["role"])
    op.create_index("idx_users_is_active", "users", ["is_active"])


def downgrade() -> None:
    """Downgrade schema."""
    # Items table
    op.drop_index("idx_items_id", table_name="items")
    op.drop_index("idx_items_owner_id", table_name="items")
    op.drop_index("idx_items_price", table_name="items")
    op.drop_index("idx_items_description", table_name="items")
    op.drop_index("idx_items_title", table_name="items")

    # Users table
    op.drop_index("idx_users_is_active", table_name="users")
    op.drop_index("idx_users_role", table_name="users")
    op.drop_index("idx_users_full_name", table_name="users")
    op.drop_index("idx_users_email", table_name="users")
