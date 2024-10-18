"""empty message

Revision ID: 070315e1488a
Revises: c20382d1f775
Create Date: 2024-10-18 03:11:32.097217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '070315e1488a'
down_revision: Union[str, None] = 'c20382d1f775'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_data_extended', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('user_data_extended_id_fkey', 'user_data_extended', type_='foreignkey')
    op.create_foreign_key(None, 'user_data_extended', 'user', ['user_id'], ['id'], ondelete='cascade')
    op.drop_column('user_data_extended', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_data_extended', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user_data_extended', type_='foreignkey')
    op.create_foreign_key('user_data_extended_id_fkey', 'user_data_extended', 'user', ['id'], ['id'], ondelete='CASCADE')
    op.drop_column('user_data_extended', 'user_id')
    # ### end Alembic commands ###
