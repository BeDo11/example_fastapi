"""add content column to posts table

Revision ID: 7718b029383f
Revises: 781bba487cd1
Create Date: 2023-07-09 13:59:13.116950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7718b029383f'
down_revision = '781bba487cd1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
