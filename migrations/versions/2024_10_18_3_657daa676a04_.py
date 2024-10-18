"""empty message

Revision ID: 657daa676a04
Revises: e29894b5a3cc
Create Date: 2024-10-18 05:37:02.280838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '657daa676a04'
down_revision: Union[str, None] = 'e29894b5a3cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('friend_ship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user1_id', sa.Integer(), nullable=False),
    sa.Column('user2_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['user1_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('user', 'sent_friend_request')
    op.drop_column('user', 'received_friend_requests')
    op.drop_column('user', 'friend_list')
    op.create_unique_constraint(None, 'user_data_extended', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_data_extended', type_='unique')
    op.add_column('user', sa.Column('friend_list', postgresql.ARRAY(sa.INTEGER()), server_default=sa.text("'{}'::integer[]"), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('received_friend_requests', postgresql.ARRAY(sa.INTEGER()), server_default=sa.text("'{}'::integer[]"), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('sent_friend_request', postgresql.ARRAY(sa.INTEGER()), server_default=sa.text("'{}'::integer[]"), autoincrement=False, nullable=False))
    op.drop_table('friend_ship')
    op.drop_table('friend_request')
    # ### end Alembic commands ###
