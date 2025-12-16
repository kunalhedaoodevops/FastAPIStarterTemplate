"""initial

Revision ID: 95b0c300827d
Revises:
Create Date: 2025-12-14 23:36:49.217285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95b0c300827d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('role', sa.String(50), nullable=False, server_default='user')
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('price', sa.Float, nullable=False, server_default='0'),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )

    op.create_table(
        "filestore",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("stored_filename", sa.String(length=255), nullable=False, unique=True),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("client_ip", sa.String(length=45), nullable=True),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_filestore_stored_filename",
        "filestore",
        ["stored_filename"],
        unique=True,
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('items')
    op.drop_table('users')
    op.drop_index("ix_filestore_stored_filename", table_name="filestore")
    op.drop_table("filestore")