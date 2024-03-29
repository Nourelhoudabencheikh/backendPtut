"""fixer due to sqlalchemy 2 0 migration

Revision ID: 8b2122f28c47
Revises: 0f2ddfa2608f
Create Date: 2024-03-06 17:29:36.832011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision= '8b2122f28c47'
down_revision = '0f2ddfa2608f'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def upgrade_() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
      with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade_() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###