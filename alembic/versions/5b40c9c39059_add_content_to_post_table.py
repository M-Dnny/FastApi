"""add content to post table

Revision ID: 5b40c9c39059
Revises: 01a56dbed714
Create Date: 2022-08-20 12:39:35.531963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b40c9c39059'
down_revision = '01a56dbed714'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
