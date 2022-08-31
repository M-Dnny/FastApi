"""added profile column in user table

Revision ID: 9f8f32b46921
Revises: 9b4aa4ad7da6
Create Date: 2022-08-31 01:36:06.802955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f8f32b46921'
down_revision = '9b4aa4ad7da6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('image_path', sa.String(), nullable=True))
    op.add_column('users', sa.Column('image_url', sa.String(), nullable=True))
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=b'I00\n')
    # op.drop_column('users', 'profile_image_url')
    # op.drop_column('users', 'profile_image_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_image_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('profile_image_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('users', 'image_url')
    op.drop_column('users', 'image_path')
    # ### end Alembic commands ###