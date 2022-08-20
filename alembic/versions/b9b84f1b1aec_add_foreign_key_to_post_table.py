"""add foreign-key to post table

Revision ID: b9b84f1b1aec
Revises: 891f290f88e6
Create Date: 2022-08-20 12:48:12.990046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9b84f1b1aec'
down_revision = '891f290f88e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
