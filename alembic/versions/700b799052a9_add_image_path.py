"""add image_path

Revision ID: 700b799052a9
Revises: 0804e03238aa
Create Date: 2022-08-30 22:43:45.765866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '700b799052a9'
down_revision = '0804e03238aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=b'I00\n')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('profile')
    # ### end Alembic commands ###