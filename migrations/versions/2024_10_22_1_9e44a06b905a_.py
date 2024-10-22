"""empty message

Revision ID: 9e44a06b905a
Revises: 3739b9bc1023
Create Date: 2024-10-22 15:45:46.053250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e44a06b905a'
down_revision: Union[str, None] = '3739b9bc1023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_table_user_chat',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'chat_id')
    )
    op.add_column('message', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('message', sa.Column('chat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'message', 'chat', ['chat_id'], ['id'])
    op.create_foreign_key(None, 'message', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_column('message', 'chat_id')
    op.drop_column('message', 'owner_id')
    op.drop_table('association_table_user_chat')
    op.drop_table('chat')
    # ### end Alembic commands ###