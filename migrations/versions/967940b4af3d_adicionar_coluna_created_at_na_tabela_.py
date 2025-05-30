"""Adicionar coluna created_at na tabela user

Revision ID: 967940b4af3d
Revises: 
Create Date: 2025-04-30 23:45:16.878935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '967940b4af3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_lesson', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('completed_lessons', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('last_accessed', sa.DateTime(), nullable=True))
        batch_op.drop_column('points')
        batch_op.drop_column('level')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('phone_number',
               existing_type=sa.VARCHAR(length=14),
               type_=sa.String(length=15),
               existing_nullable=False)
        batch_op.alter_column('confirmation_token',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=1),
               type_=sa.String(length=20),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=1),
               nullable=False)
        batch_op.alter_column('confirmation_token',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.alter_column('phone_number',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=14),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.drop_column('created_at')

    with op.batch_alter_table('progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('level', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('points', sa.INTEGER(), nullable=True))
        batch_op.drop_column('last_accessed')
        batch_op.drop_column('completed_lessons')
        batch_op.drop_column('current_lesson')

    # ### end Alembic commands ###
