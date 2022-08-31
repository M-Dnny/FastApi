"""auto generated profile

Revision ID: 816d41e2a02f
Revises: c36f21aea3a4
Create Date: 2022-08-22 23:41:03.723015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '816d41e2a02f'
down_revision = 'c36f21aea3a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
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
