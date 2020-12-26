"""empty message

Revision ID: 775e291e760f
Revises: 742c66e23b3f
Create Date: 2020-12-26 16:50:21.389936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '775e291e760f'
down_revision = '742c66e23b3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###