"""added new fields in the review and comment tables

Revision ID: c782e827c835
Revises: 50f96270aa53
Create Date: 2023-06-08 21:03:36.723218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c782e827c835'
down_revision = '50f96270aa53'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('status', sa.Boolean(), nullable=True))
    op.add_column('reviews', sa.Column('is_reviewed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'is_reviewed')
    op.drop_column('comments', 'status')
    # ### end Alembic commands ###
