"""changed table for package

Revision ID: 8be4c2baf7f8
Revises: d2e465498943
Create Date: 2023-06-07 12:06:23.645665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8be4c2baf7f8'
down_revision = 'd2e465498943'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packages', sa.Column('start_time', sa.String(), nullable=True))
    op.add_column('packages', sa.Column('end_time', sa.String(), nullable=True))
    op.drop_column('packages', 'night_time')
    op.drop_column('packages', 'day_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packages', sa.Column('day_time', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('packages', sa.Column('night_time', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('packages', 'end_time')
    op.drop_column('packages', 'start_time')
    # ### end Alembic commands ###