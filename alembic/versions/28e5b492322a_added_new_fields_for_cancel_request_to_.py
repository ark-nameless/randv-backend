"""added new fields for cancel request to accomodatethe refund amount in the reservaion cancellation.

Revision ID: 28e5b492322a
Revises: c782e827c835
Create Date: 2023-06-09 15:01:47.988446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28e5b492322a'
down_revision = 'c782e827c835'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cancel_requests', sa.Column('refund_amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cancel_requests', 'refund_amount')
    # ### end Alembic commands ###
