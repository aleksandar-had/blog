"""about_me and last_seen fields added to user model

Revision ID: 295206c04c4c
Revises: 3328db68f91e
Create Date: 2020-07-25 13:23:27.286477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '295206c04c4c'
down_revision = '3328db68f91e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
