"""create posts table

Revision ID: b316489adf69
Revises: 
Create Date: 2022-08-15 16:50:55.670289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b316489adf69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(255), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
