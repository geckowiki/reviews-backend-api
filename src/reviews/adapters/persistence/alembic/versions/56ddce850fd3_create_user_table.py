"""create user table

Revision ID: 56ddce850fd3
Revises: 
Create Date: 2022-09-10 00:12:36.752136

"""
from alembic import op
import sqlalchemy as sa

from fastapi_users_db_sqlalchemy.generics import GUID


# revision identifiers, used by Alembic.
revision = '56ddce850fd3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', GUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__user'))
    )
    op.create_index(op.f('ix__user__email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__user__email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
