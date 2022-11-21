from app.models import *
from tests.base_test_case import BaseTestCase
from tests.test_data_generator import *
import copy

class TestAddSubject(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/subject/', json=subject_schema, headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.post('/subject/', json=subject_schema)
        self.assert401(response)

    def test_invalid_already_exists(self):
        add_test_subject(subject_schema)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/subject/', json=subject_schema, headers=self.auth_header)
        self.assert400(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/subject/', json=subject_schema, headers=self.auth_header)
        self.assert403(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/subject/', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)
    
    def test_invalid_teacher(self):
        super().auth(admin_login_path, admin_credentials)
        invalid_teacher_schema = copy.deepcopy(subject_schema)
        invalid_teacher_schema['teacher_ids'].append(20)
        response = self.client.post('/subject/', json=invalid_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_several_teachers(self):
        add_test_teacher(teacher_schema)
        add_test_teacher(teacher_with_subject_schema)
        super().auth(admin_login_path, admin_credentials)
        curr_teacher_schema = copy.deepcopy(subject_schema)
        curr_teacher_schema['teacher_ids'].append(1)
        curr_teacher_schema['teacher_ids'].append(2)
        response = self.client.post('/subject/', json=curr_teacher_schema, headers=self.auth_header)
        self.assert200(response)

class TestGetSubject(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_subject(subject_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/subject/1', headers=self.auth_header)
        self.assert200(response)

    def test_invalid_id(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/subject/20', headers=self.auth_header)
        self.assert404(response)
class TestUpdateSubject(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_subject(subject_schema)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/subject/1', json=subject_schema, headers=self.auth_header)
        self.assert403(response)

    def test_already_exists(self):
        add_test_subject(subject2_schema)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/subject/1', json=subject2_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_teacher(self):
        super().auth(admin_login_path, admin_credentials)
        invalid_teacher_schema = copy.deepcopy(subject_schema)
        invalid_teacher_schema['teacher_ids'].append(20)
        response = self.client.post('/subject/1', json=invalid_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        current_subject_schema = copy.deepcopy(subject_schema)
        current_subject_schema['teacher_ids'].append(1)
        response = self.client.post('/subject/1', json=subject_schema, headers=self.auth_header)
        self.assert200(response)

    def test_no_subject(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/subject/20', json=subject_schema, headers=self.auth_header)
        self.assert404(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/subject/1', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)
class TestDeleteSubject(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_subject(subject_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/subject/1', headers=self.auth_header)
        self.assertStatus(response, 204)

    def test_invalid_id(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/subject/20', headers=self.auth_header)
        self.assert404(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.delete('/subject/1', headers=self.auth_header)
        self.assert403(response)
