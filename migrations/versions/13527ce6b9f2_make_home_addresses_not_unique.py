"""make home addresses not unique

Revision ID: 13527ce6b9f2
Revises: 52c894204927
Create Date: 2018-02-14 06:05:20.356332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13527ce6b9f2'
down_revision = '52c894204927'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_home_address', table_name='user')
    op.create_index(op.f('ix_user_home_address'), 'user', ['home_address'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_home_address'), table_name='user')
    op.create_index('ix_user_home_address', 'user', ['home_address'], unique=1)
    # ### end Alembic commands ###
