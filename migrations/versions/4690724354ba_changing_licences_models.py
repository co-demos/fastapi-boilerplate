"""changing licences models

Revision ID: 4690724354ba
Revises: 47deac221ff8
Create Date: 2021-04-16 16:30:42.713745

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4690724354ba'
down_revision = '47deac221ff8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_licences_title', table_name='licences')
    op.create_index(op.f('ix_licences_title'), 'licences', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_licences_title'), table_name='licences')
    op.create_index('ix_licences_title', 'licences', ['title'], unique=False)
    # ### end Alembic commands ###