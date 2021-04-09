"""add locale column to users

Revision ID: 563d5d82a055
Revises: f44b614e4ebd
Create Date: 2021-04-09 14:37:31.988627

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '563d5d82a055'
down_revision = 'f44b614e4ebd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('locale', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'locale')
    # ### end Alembic commands ###
