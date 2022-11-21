from app import db
from app.models import *
from flask_bcrypt import Bcrypt

admin_login_path = '/admin/login'
student_login_path = '/student/login'

admin_credentials = {
    'login': 'admin',
    'password': 'admin'
}

admin2_credentials = {
    'login': 'admin2',
    'password' : 'admin2'
}

admin_schema = {
    **admin_credentials
}

admin2_schema = {
    **admin2_credentials
}

def add_test_admin(schema):
    db.db_session.add(Admin(login=schema['login'], password=Bcrypt().generate_password_hash(schema['password']).decode('utf-8') ))

student_credentials = {
    'login': 'user',
    'password': 'user',
}

student_schema = {
    **student_credentials,
    'info': {
        'last_name': 'Doe',
        'first_name': 'John', 
        'university_id': 1
    }
}

student2_credentials = {
    'login': 'user2',
    'password': 'user2',
}

student2_schema = {
    **student2_credentials,
    'info': {
        'last_name': 'NotDoe',
        'first_name': 'NotJohn', 
        'university_id': 1
    }
}

def add_test_student(schema):
    db.db_session.add(Student(login=schema['login'], password=Bcrypt().generate_password_hash(schema['password']).decode('utf-8'), first_name=schema['info']['first_name'], last_name=schema['info']['last_name'], university_id=schema['info']['university_id']))

university_schema = {
    'name': 'University of Test',
    'address': 'Test City'
}

def add_test_university(schema):
    db.db_session.add(University(name=schema['name'], address=schema['address']))

teacher_login_path = '/teacher/login'

teacher_credentials = {
    'login': 'teacher',
    'password': 'teacher'
}

teacher_schema = {
    **teacher_credentials,
    'info': {
        'first_name': 'First name',
        'last_name': 'Last name',
        'university_id': 1,
        'subject_ids': []
    }
}

teacher_with_subject_credentials = {
    'login': 'teacher_with_subject',
    'password' : 'teacher_with_subject'
}

teacher_with_subject_schema = {
    **teacher_with_subject_credentials,
    'info': {
        'first_name': 'First name with subject',
        'last_name': 'Last name with subject',
        'university_id': 1,
        'subject_ids': [1]
    }
}

def add_test_teacher(schema):
    db.db_session.add(Teacher(login=schema['login'], password=Bcrypt().generate_password_hash(schema['password']).decode('utf-8'), first_name=schema['info']['first_name'], last_name=schema['info']['last_name'], university_id=schema['info']['university_id']))

subject_schema = {
    'name': 'Test subject',
    'teacher_ids': []
}

subject2_schema = {
    'name': 'Test subject 2',
    'teacher_ids': []
}

def add_test_subject(schema):
    db.db_session.add(Subject(name=schema['name']))


mark_schema = {
    'student_id': 1,
    'subject_id': 1,
    'points': 5,
    'teacher_id': 1,
    'year': 2022,
    'semester': 1
}

def add_test_mark(schema):
    db.db_session.add(Mark(student_id=schema['student_id'], subject_id=schema['subject_id'], points=schema['points'], teacher_id=schema['teacher_id'], year=schema['year'], semester=schema['semester']))

def add_test_mark_to_teachers_subjects(teacher_id, subject_id):
    db.db_session.add(TeachersSubjects(teacher_id=teacher_id, subject_id=subject_id))

