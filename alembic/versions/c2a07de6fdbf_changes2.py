"""changes2

Revision ID: c2a07de6fdbf
Revises: 9604ae13a2b2
Create Date: 2024-05-14 02:12:29.033297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c2a07de6fdbf'
down_revision: Union[str, None] = '9604ae13a2b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sessions', 'exit_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('sessions', 'total_hours_spent',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sessions', 'total_coast',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sessions', 'total_coast',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('sessions', 'total_hours_spent',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('sessions', 'exit_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###