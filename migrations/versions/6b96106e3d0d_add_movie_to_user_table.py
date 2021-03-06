"""Add movie to user table

Revision ID: 6b96106e3d0d
Revises: 4bfc76bfa9b9
Create Date: 2019-10-15 11:11:19.150005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b96106e3d0d'
down_revision = '4bfc76bfa9b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('_movies', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', '_movies')
    # ### end Alembic commands ###
