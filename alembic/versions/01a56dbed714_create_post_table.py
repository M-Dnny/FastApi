"""create post table

Revision ID: 01a56dbed714
Revises: 
Create Date: 2022-08-20 12:32:26.813346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01a56dbed714'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
