"""empty message

Revision ID: 3cc90eca414e
Revises: e1621f887723
Create Date: 2021-12-08 17:29:11.688665

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3cc90eca414e'
down_revision = 'e1621f887723'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Goal')
    op.drop_table('Destination')
    op.drop_table('std_gt')
    op.drop_index('ix_Student_email', table_name='Student')
    op.drop_index('ix_Student_last_name', table_name='Student')
    op.drop_table('Student')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    op.add_column('Todo', sa.Column('status_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Todo', 'Status', ['status_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Todo', type_='foreignkey')
    op.drop_column('Todo', 'status_id')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('registered_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_super_user', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('school_logo_name', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('matya_logo_name', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.create_table('Student',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('birth_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('grade', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('background', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('profetional', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['general_txt.id'], name='Student_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Student_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_Student_last_name', 'Student', ['last_name'], unique=False)
    op.create_index('ix_Student_email', 'Student', ['email'], unique=False)
    op.create_table('std_gt',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('gt_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('due_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('selected', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('hide', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['gt_id'], ['general_txt.id'], name='std_gt_gt_id_fkey'),
    sa.ForeignKeyConstraint(['status_id'], ['Status.id'], name='std_gt_status_id_fkey'),
    sa.ForeignKeyConstraint(['student_id'], ['Student.id'], name='std_gt_student_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='std_gt_pkey')
    )
    op.create_table('Destination',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['general_txt.id'], name='Destination_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Destination_pkey')
    )
    op.create_table('Goal',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['general_txt.id'], name='Goal_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Goal_pkey')
    )
    # ### end Alembic commands ###