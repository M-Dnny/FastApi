"""add last few to post table

Revision ID: 5c901a2c63d9
Revises: b9b84f1b1aec
Create Date: 2022-08-20 12:51:35.295025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c901a2c63d9'
down_revision = 'b9b84f1b1aec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
