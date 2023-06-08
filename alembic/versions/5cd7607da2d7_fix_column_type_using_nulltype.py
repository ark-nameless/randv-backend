"""Fix column type using NullType

Revision ID: 5cd7607da2d7
Revises: c0348d42d3df
Create Date: 2023-06-07 09:50:45.754661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd7607da2d7'
down_revision = 'c0348d42d3df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.alter_column('total_amount', 'total_amount', type_=sa.Integer()) # type: ignore
    # op.alter_column('reference_no', 'reference_no', type_=sa.String()) # type: ignore
    pass

def downgrade() -> None:
    pass
