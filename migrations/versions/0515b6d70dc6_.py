"""empty message

Revision ID: 0515b6d70dc6
Revises: b1a315b60919
Create Date: 2024-03-18 21:18:34.724819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0515b6d70dc6'
down_revision = 'b1a315b60919'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=20), nullable=True),
    sa.Column('skin_color', sa.String(length=20), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.Column('birth_year', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('homeworld', sa.String(length=250), nullable=True),
    sa.Column('character_pic', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=20), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=20), nullable=True),
    sa.Column('terrain', sa.String(length=20), nullable=True),
    sa.Column('surface_water', sa.String(), nullable=True),
    sa.Column('planet_pic', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('task')
    op.drop_table('todo_list')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('character_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])
        batch_op.create_foreign_key(None, 'character', ['character_id'], ['id'])
        batch_op.drop_column('full_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.VARCHAR(length=240), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('username',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('planet_id')
        batch_op.drop_column('character_id')
        batch_op.drop_column('password')
        batch_op.drop_column('email')

    op.create_table('todo_list',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('todo_list_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='todo_list_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='todo_list_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('task',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('label', sa.VARCHAR(length=240), autoincrement=False, nullable=True),
    sa.Column('done', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('todo_list_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['todo_list_id'], ['todo_list.id'], name='task_todo_list_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='task_pkey')
    )
    op.drop_table('favorite')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###
