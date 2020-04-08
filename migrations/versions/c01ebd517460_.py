"""empty message

Revision ID: c01ebd517460
Revises: 
Create Date: 2020-04-05 23:23:31.106799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c01ebd517460'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('horoscope',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('sign', sa.String(length=50), nullable=True),
    sa.Column('download_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('horoscope')
    # ### end Alembic commands ###