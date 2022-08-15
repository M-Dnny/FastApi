"""add foreign key to post table

Revision ID: 0e9accd9f79c
Revises: b1ce1073bcc0
Create Date: 2022-08-15 17:39:21.812457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e9accd9f79c'
down_revision = 'b1ce1073bcc0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_users.fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users.fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
