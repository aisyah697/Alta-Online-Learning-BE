"""a

Revision ID: adbae493b2d2
Revises: 58628d9cec45
Create Date: 2020-06-27 11:36:13.351540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adbae493b2d2'
down_revision = '58628d9cec45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('histories_subject', sa.Column('lock_key', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('histories_subject', 'lock_key')
    # ### end Alembic commands ###