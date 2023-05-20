"""FastLinks: Add table

Revision ID: 8bedc0096de1
Revises: 
Create Date: 2023-05-20 21:43:07.110951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bedc0096de1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fast_links',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.Text(length=10), nullable=False),
    sa.Column('url', sa.Text(length=255), nullable=False),
    sa.Column('expire', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fast_links')
    # ### end Alembic commands ###