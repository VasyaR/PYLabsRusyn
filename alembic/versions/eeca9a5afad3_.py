"""empty message

Revision ID: eeca9a5afad3
Revises: 7b8431c3d05b
Create Date: 2022-10-26 21:33:44.056150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeca9a5afad3'
down_revision = '7b8431c3d05b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('marks_student_id_fkey', 'marks', type_='foreignkey')
    op.drop_constraint('marks_subject_id_fkey', 'marks', type_='foreignkey')
    op.drop_constraint('marks_teacher_id_fkey', 'marks', type_='foreignkey')
    op.create_foreign_key(None, 'marks', 'subjects', ['subject_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'marks', 'teachers', ['teacher_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'marks', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('students_university_id_fkey', 'students', type_='foreignkey')
    op.create_foreign_key(None, 'students', 'universities', ['university_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('teachers_university_id_fkey', 'teachers', type_='foreignkey')
    op.create_foreign_key(None, 'teachers', 'universities', ['university_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('teachers_subjects_subject_id_fkey', 'teachers_subjects', type_='foreignkey')
    op.drop_constraint('teachers_subjects_teacher_id_fkey', 'teachers_subjects', type_='foreignkey')
    op.create_foreign_key(None, 'teachers_subjects', 'subjects', ['subject_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'teachers_subjects', 'teachers', ['teacher_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teachers_subjects', type_='foreignkey')
    op.drop_constraint(None, 'teachers_subjects', type_='foreignkey')
    op.create_foreign_key('teachers_subjects_teacher_id_fkey', 'teachers_subjects', 'teachers', ['teacher_id'], ['id'])
    op.create_foreign_key('teachers_subjects_subject_id_fkey', 'teachers_subjects', 'subjects', ['subject_id'], ['id'])
    op.drop_constraint(None, 'teachers', type_='foreignkey')
    op.create_foreign_key('teachers_university_id_fkey', 'teachers', 'universities', ['university_id'], ['id'])
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.create_foreign_key('students_university_id_fkey', 'students', 'universities', ['university_id'], ['id'])
    op.drop_constraint(None, 'marks', type_='foreignkey')
    op.drop_constraint(None, 'marks', type_='foreignkey')
    op.drop_constraint(None, 'marks', type_='foreignkey')
    op.create_foreign_key('marks_teacher_id_fkey', 'marks', 'teachers', ['teacher_id'], ['id'])
    op.create_foreign_key('marks_subject_id_fkey', 'marks', 'subjects', ['subject_id'], ['id'])
    op.create_foreign_key('marks_student_id_fkey', 'marks', 'students', ['student_id'], ['id'])
    # ### end Alembic commands ###
