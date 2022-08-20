"""add user table

Revision ID: 891f290f88e6
Revises: 5b40c9c39059
Create Date: 2022-08-20 12:45:10.490926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '891f290f88e6'
down_revision = '5b40c9c39059'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
