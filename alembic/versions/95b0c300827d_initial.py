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
    # --------------------
    # Sample data
    # --------------------
    users_table = sa.table(
        "users",
        sa.column("id", sa.Integer),
        sa.column("email", sa.String),
        sa.column("full_name", sa.String),
        sa.column("hashed_password", sa.String),
        sa.column("is_active", sa.Boolean),
        sa.column("role", sa.String),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "id": 1,
                "email": "admin@example.com",
                "full_name": "Admin User",
                "hashed_password": "$pbkdf2-sha256$29000$l/IeA8DYe4.xNiaEcC6FUA$L/1exwVPaQ5FTnnAdAJZfqFzdr8VssjTIn6otONQjD8",
                "is_active": True,
                "role": "admin",
            },
            {
                "id": 2,
                "email": "user@example.com",
                "full_name": "Normal User",
                "hashed_password": "$pbkdf2-sha256$29000$PEdIydm7d87Zu3du7R0D4A$zNHC57tbd.h5XKlXeFDHVbGUJVSqd67I721GxIRJoG4",
                "is_active": True,
                "role": "user",
            },
        ],
    )

    items_table = sa.table(
        "items",
        sa.column("id", sa.Integer),
        sa.column("title", sa.String),
        sa.column("description", sa.Text),
        sa.column("price", sa.Float),
        sa.column("owner_id", sa.Integer),
    )

    op.bulk_insert(
        items_table,
        [
            {
                "id": 1,
                "title": "Sample Item 1",
                "description": "First sample item",
                "price": 100.0,
                "owner_id": 1,
            },
            {
                "id": 2,
                "title": "Sample Item 2",
                "description": "Second sample item",
                "price": 50.0,
                "owner_id": 2,
            },
        ],
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('items')
    op.drop_table('users')
    op.drop_index("ix_filestore_stored_filename", table_name="filestore")
    op.drop_table("filestore")