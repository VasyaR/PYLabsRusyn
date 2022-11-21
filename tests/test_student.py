from app.models import *
from tests.base_test_case import BaseTestCase
from tests.test_data_generator import *

invalid_student_credentials = {
    'login': 'user2',
    'password': 'user2',
}

invalid_student_schema = {
    **invalid_student_credentials,
    'info': {
        'last_name': 'NotDoe',
        'first_name': 'NotJohn', 
        'university_id': 2
    }
}

class TestAddAStudent(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/', json=student_schema, headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.post('/student/', json=student_schema)
        self.assert401(response)

    def test_invalid_no_data(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/', json=None, headers=self.auth_header)
        self.assert400(response)
        
    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/student/', json=student_schema, headers=self.auth_header)
        self.assert403(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)
    
    def test_already_exists(self):
        add_test_student(student_schema)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/', json=student_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_university_id(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/', json=invalid_student_schema, headers=self.auth_header)
        self.assert400(response)

class TestGetStudent(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)
        add_test_admin(admin_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/student/1', headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        response = self.client.get('/student/1')
        self.assert401(response)

    def test_no_permissions(self):
        add_test_student(student2_schema)
        super().auth(student_login_path, student2_credentials)
        response = self.client.get('/student/1', headers=self.auth_header)
        self.assert403(response)

    def test_not_found(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/student/2', headers=self.auth_header)
        self.assert404(response)

class TestUpdateStudent(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)
        add_test_admin(admin_schema)
        self.schema = {'password': 'password'}

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/1', json=self.schema, headers=self.auth_header)
        self.assertStatus(response, 201)

    def test_invalid_no_credentials(self):
        response = self.client.post('/student/1', json=self.schema)
        self.assert401(response)

    def test_no_permissions(self):
        add_test_student(student2_schema)
        super().auth(student_login_path, student2_credentials)
        response = self.client.post('/student/1', json=self.schema, headers=self.auth_header)
        self.assert403(response)

    def test_not_found(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/2', json=self.schema, headers=self.auth_header)
        self.assert404(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/student/1', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

class TestDeleteStudent(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)
        add_test_admin(admin_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/student/1', headers=self.auth_header)
        self.assertStatus(response, 204)

    def test_invalid_no_credentials(self):
        response = self.client.delete('/student/1')
        self.assert401(response)

    def test_no_permissions(self):
        add_test_student(student2_schema)
        super().auth(student_login_path, student2_credentials)
        response = self.client.delete('/student/1', headers=self.auth_header)
        self.assert403(response)

    def test_not_found(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/student/2', headers=self.auth_header)
        self.assert404(response)

class TestGetStudentRating(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)
        add_test_admin(admin_schema)
        add_test_mark(mark_schema)
        self.date_schema = {'year': 2022, 'semester': 1}
        self.path = '/student/1/subject/1/points'

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get(self.path, query_string=self.date_schema, headers=self.auth_header)
        (response.json)
        self.assert200(response)

    def test_no_permissions(self):
        add_test_student(student2_schema)
        super().auth(student_login_path, student2_credentials)
        response = self.client.get(self.path, query_string=self.date_schema, headers=self.auth_header)
        self.assert403(response)

    def test_not_found(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get(self.path, query_string={'year': 1999, 'semester': 1}, headers=self.auth_header)
        self.assert404(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get(self.path, query_string={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

class TestUpdateSubjectPoints(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)
        add_test_teacher(teacher_schema)
        add_test_subject(subject_schema)
        add_test_mark(mark_schema)
        add_test_mark_to_teachers_subjects(1,1)
        self.path = '/student/1/subject/1/points'
        self.update_mark_schema = {'year': 2022, 'semester': 1, 'points': 5}
        
    def test_success(self):
        super().auth(teacher_login_path, teacher_credentials)
        response = self.client.post(self.path, json=self.update_mark_schema, headers=self.auth_header)
        self.assertStatus(response, 201)

    def test_no_permissions(self):
        add_test_teacher(teacher_with_subject_schema)
        super().auth(teacher_login_path, teacher_with_subject_credentials)
        response = self.client.post(self.path, json=self.update_mark_schema, headers=self.auth_header)
        self.assert403(response)

    def test_no_permissions_student(self):
        super().auth(student_login_path, student_credentials)
        response = self.client.post(self.path, json=self.update_mark_schema, headers=self.auth_header)
        self.assert403(response)

    def test_not_found(self):
        super().auth(teacher_login_path, teacher_credentials)
        response = self.client.post('/student/2/subject/1/points', json=self.update_mark_schema, headers=self.auth_header)
        self.assert404(response)

    def test_invalid_request(self):
        super().auth(teacher_login_path, teacher_credentials)
        response = self.client.post(self.path, json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

class TestStudentAuth(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)

    def test_success(self):
        response = self.client.post('/student/login', json=student_credentials)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        response = self.client.post('/student/login', json={})
        self.assert400(response)

    def test_invalid_login(self):
        response = self.client.post('/student/login', json={'login': 'bad', 'password': 'bad'})
        self.assert404(response)

    def test_invalid_incorect_password(self):
        response = self.client.post('/student/login', json={'login': student_schema['login'], 'password': 'bad'})
        self.assert401(response)

class TestGetStudentRating(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_student(student_schema)
        add_test_admin(admin_schema)
        add_test_mark(mark_schema)
        self.date_schema = {'year': 2022, 'semester': 1}
        self.path = '/student/1/subject/1/points'

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get(self.path, query_string=self.date_schema, headers=self.auth_header)
        self.assert200(response)

    def test_no_permissions(self):
        add_test_student(student2_schema)
        super().auth(student_login_path, student2_credentials)
        response = self.client.get(self.path, query_string=self.date_schema, headers=self.auth_header)
        self.assert403(response)

    def test_not_found(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get(self.path, query_string={'year': 1999, 'semester': 1}, headers=self.auth_header)
        self.assert404(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get(self.path, query_string={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

