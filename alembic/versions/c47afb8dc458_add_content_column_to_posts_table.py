"""add content column to posts table

Revision ID: c47afb8dc458
Revises: c56d38af9927
Create Date: 2026-06-17 20:39:31.126118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c47afb8dc458'
down_revision: Union[str, Sequence[str], None] = 'c56d38af9927'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')