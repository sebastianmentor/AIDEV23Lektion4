"""Initial Migration

Revision ID: 703d9159b356
Revises: 
Create Date: 2024-04-02 09:14:02.894155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '703d9159b356'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    # ### end Alembic commands ###
