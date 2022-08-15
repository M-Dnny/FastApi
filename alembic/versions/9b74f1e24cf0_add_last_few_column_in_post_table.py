"""add last few column in post table

Revision ID: 9b74f1e24cf0
Revises: 0e9accd9f79c
Create Date: 2022-08-15 18:20:01.118168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b74f1e24cf0'
down_revision = '0e9accd9f79c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default=sa.text('True')))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
