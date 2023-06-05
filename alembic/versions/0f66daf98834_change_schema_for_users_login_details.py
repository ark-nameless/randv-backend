"""change schema for users login details

Revision ID: 0f66daf98834
Revises: fe63a568fd07
Create Date: 2023-06-05 09:22:01.578487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f66daf98834'
down_revision = 'fe63a568fd07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_items_description', table_name='items')
    op.drop_index('ix_items_id', table_name='items')
    op.drop_index('ix_items_title', table_name='items')
    op.drop_table('items')
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.add_column('users', sa.Column('access', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('users', sa.Column('reset_token', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'reset_token')
    op.drop_column('users', 'access')
    op.drop_column('users', 'username')
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='items_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_index('ix_items_title', 'items', ['title'], unique=False)
    op.create_index('ix_items_id', 'items', ['id'], unique=False)
    op.create_index('ix_items_description', 'items', ['description'], unique=False)
    # ### end Alembic commands ###