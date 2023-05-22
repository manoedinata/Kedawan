"""Update tables

Revision ID: d92f570798f3
Revises: 0fd6deae526a
Create Date: 2023-05-22 21:45:57.416655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd92f570798f3'
down_revision = '0fd6deae526a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ip_address_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.VARBINARY(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip_address')
    )
    with op.batch_alter_table('visitor', schema=None) as batch_op:
        batch_op.drop_constraint('visitor_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'fast_links', ['fast_links_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visitor', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('visitor_ibfk_1', 'fast_links', ['fast_links_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    op.drop_table('ip_address_log')
    # ### end Alembic commands ###