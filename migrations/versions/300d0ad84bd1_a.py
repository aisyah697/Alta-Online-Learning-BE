"""a

Revision ID: 300d0ad84bd1
Revises: 
Create Date: 2020-07-03 08:10:54.655800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '300d0ad84bd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('histories_altatest', sa.Column('time_start', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('histories_altatest', 'time_start')
    # ### end Alembic commands ###