"""add foreign key to posts table

Revision ID: 9e1ade1af514
Revises: f9dec75ca546
Create Date: 2023-07-09 14:21:36.446669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e1ade1af514'
down_revision = 'f9dec75ca546'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    #op.drop_constraint('post_users_fk', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
