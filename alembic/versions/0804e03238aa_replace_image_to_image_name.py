"""replace image to image_name

Revision ID: 0804e03238aa
Revises: 7797f2fb6c0c
Create Date: 2022-08-28 21:22:16.781382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0804e03238aa'
down_revision = '7797f2fb6c0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.String(), nullable=True),
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