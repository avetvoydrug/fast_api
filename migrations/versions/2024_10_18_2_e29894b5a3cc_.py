"""empty message

Revision ID: e29894b5a3cc
Revises: 070315e1488a
Create Date: 2024-10-18 03:21:09.728816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e29894b5a3cc'
down_revision: Union[str, None] = '070315e1488a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_data_extended',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('unique_id', sa.String(length=58), nullable=True),
    sa.Column('birth_date', sa.DATE(), nullable=True),
    sa.Column('sex', sa.Enum('male', 'female', 'other', name='sexenum'), nullable=True),
    sa.Column('relat_status', sa.Enum('single', 'in_a_relationship', 'married', 'engaged', 'it_s_complicated', 'separated', 'divorced', 'widowed', 'open_to_dating', 'friend_zone', 'looking_for_friends', 'other', name='relationshipstatusenum'), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('education', sa.String(length=100), nullable=True),
    sa.Column('interests', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('unique_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_data_extended')
    # ### end Alembic commands ###
