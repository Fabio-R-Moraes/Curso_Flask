"""empty message

Revision ID: 99786e9053f6
Revises: fea723575263
Create Date: 2024-07-31 19:49:28.330719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99786e9053f6'
down_revision = 'fea723575263'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('sobrenome', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('senha', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
