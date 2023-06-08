"""change arrival date to striring

Revision ID: fc5bee77ef4e
Revises: 590f7fd115e8
Create Date: 2023-06-07 14:45:09.635312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc5bee77ef4e'
down_revision = '590f7fd115e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('reservations', 'arrival')
    op.drop_column('reservations', 'departure')
    op.add_column('reservations', sa.Column('arrival', sa.String(), nullable=True))
    op.add_column('reservations', sa.Column('departure', sa.String(), nullable=True))


def downgrade() -> None:
    pass
