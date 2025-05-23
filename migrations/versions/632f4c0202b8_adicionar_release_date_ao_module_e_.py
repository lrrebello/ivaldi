"""Adicionar release_date ao Module e criar TestResult

Revision ID: 632f4c0202b8
Revises: 967940b4af3d
Create Date: 2025-05-01 00:05:34.457722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '632f4c0202b8'
down_revision = '967940b4af3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.add_column(sa.Column('release_date', sa.DateTime(), nullable=True))

    with op.batch_alter_table('progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('level', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('lessons_completed', sa.Integer(), nullable=True))
        batch_op.drop_column('completed_lessons')
        batch_op.drop_column('last_accessed')
        batch_op.drop_column('current_lesson')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('state', sa.String(length=100), nullable=False))
        batch_op.alter_column('confirmation_token',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('confirmation_token',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.drop_column('state')
        batch_op.drop_column('city')

    with op.batch_alter_table('progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_lesson', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('last_accessed', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('completed_lessons', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('lessons_completed')
        batch_op.drop_column('level')

    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.drop_column('release_date')

    # ### end Alembic commands ###
