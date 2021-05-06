"""add tablemeta table

Revision ID: 6d253843cadf
Revises: ae7472e1e9cb
Create Date: 2021-05-06 13:39:20.907699

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '6d253843cadf'
down_revision = 'ae7472e1e9cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tablemetas', sa.Column('table_data', sa.String(), nullable=True))
    op.create_index(op.f('ix_tablemetas_table_data'), 'tablemetas', ['table_data'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tablemetas_table_data'), table_name='tablemetas')
    op.drop_column('tablemetas', 'table_data')
    # ### end Alembic commands ###
