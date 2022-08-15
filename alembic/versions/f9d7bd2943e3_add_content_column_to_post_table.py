"""add content column to post table

Revision ID: f9d7bd2943e3
Revises: b316489adf69
Create Date: 2022-08-15 17:08:54.304426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9d7bd2943e3'
down_revision = 'b316489adf69'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(255), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
