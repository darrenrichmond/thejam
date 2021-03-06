"""events and venues tables

Revision ID: 52c894204927
Revises: 7b8377d433cc
Create Date: 2018-02-12 14:23:57.581607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52c894204927'
down_revision = '7b8377d433cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_venue_name'), 'venue', ['name'], unique=True)
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('night', sa.String(length=10), nullable=True),
    sa.Column('recurs', sa.String(length=32), nullable=True),
    sa.Column('start_time', sa.String(length=8), nullable=True),
    sa.Column('end_time', sa.String(length=8), nullable=True),
    sa.Column('adv_signup', sa.String(length=8), nullable=True),
    sa.Column('notes', sa.String(length=128), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_night'), 'event', ['night'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_event_night'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_venue_name'), table_name='venue')
    op.drop_table('venue')
    # ### end Alembic commands ###
