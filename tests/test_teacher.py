from app.models import *
from tests.base_test_case import BaseTestCase
from tests.test_data_generator import *
import copy

invalid_teacher_schema = teacher_schema.copy()
del invalid_teacher_schema['info']

class TestAddTeacher(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)

    def test_success(self):
        add_test_subject(subject_schema)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/teacher/', json=teacher_with_subject_schema, headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.post('/teacher/', json=teacher_schema)
        self.assert401(response)

    def test_invalid_university(self):
        super().auth(admin_login_path, admin_credentials)
        invalid_uni_teacher_schema = copy.deepcopy(teacher_schema)
        invalid_uni_teacher_schema['info']['university_id'] = 2
        response = self.client.post('/teacher/', json=invalid_uni_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_subject(self):
        super().auth(admin_login_path, admin_credentials)
        invalid_sub_teacher_schema = copy.deepcopy(teacher_with_subject_schema)
        invalid_sub_teacher_schema['info']['subject_ids'][0] = 2
        response = self.client.post('/teacher/', json=invalid_sub_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/teacher/', json=invalid_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/teacher/', json=teacher_schema, headers=self.auth_header)
        self.assert403(response)

    def test_already_exists(self):
        add_test_teacher(teacher_schema)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/teacher/', json=teacher_schema, headers=self.auth_header)
        self.assert400(response)

class TestGetTeacher(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_teacher(teacher_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/teacher/1', headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.get('/teacher/1')
        self.assert401(response)

    def test_invalid_teacher(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/teacher/2', headers=self.auth_header)
        self.assert404(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.get('/teacher/1', headers=self.auth_header)
        self.assert403(response)

class TestUpdateTeacher(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_teacher(teacher_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        temp_teacher_schema = {}
        temp_teacher_schema['first_name'] = teacher_schema['info']['first_name']
        temp_teacher_schema['last_name'] = teacher_schema['info']['last_name']
        temp_teacher_schema['university_id'] = teacher_schema['info']['university_id']
        temp_teacher_schema['subject_ids'] = teacher_schema['info']['subject_ids']
        response = self.client.post('/teacher/1', json=temp_teacher_schema, headers=self.auth_header)
        self.assertStatus(response, 201)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.post('/teacher/1', json=teacher_schema)
        self.assert401(response)

    def test_invalid_teacher(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/teacher/2', json=teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_university(self):
        super().auth(admin_login_path, admin_credentials)
        invalid_uni_teacher_schema = copy.deepcopy(teacher_schema['info'])
        invalid_uni_teacher_schema['university_id'] = 2
        response = self.client.post('/teacher/1', json=invalid_uni_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_subject(self):
        super().auth(admin_login_path, admin_credentials)
        invalid_sub_teacher_schema = copy.deepcopy(teacher_with_subject_schema['info'])
        invalid_sub_teacher_schema['subject_ids'][0] = 2
        response = self.client.post('/teacher/1', json=invalid_sub_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/teacher/1', json=invalid_teacher_schema, headers=self.auth_header)
        self.assert400(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/teacher/1', json=teacher_schema, headers=self.auth_header)
        self.assert403(response)

class TestDeleteTeacher(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_teacher(teacher_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/teacher/1', headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.delete('/teacher/1')
        self.assert401(response)

    def test_invalid_teacher(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/teacher/2', headers=self.auth_header)
        self.assert404(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.delete('/teacher/1', headers=self.auth_header)
        self.assert403(response)


class TestAuthTeacher(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)
        add_test_teacher(teacher_schema)

    def test_success(self):
        response = self.client.post(teacher_login_path, json=teacher_credentials)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        response = self.client.post(teacher_login_path, json={})
        self.assert400(response)

    def test_invalid_teacher(self):
        response = self.client.post(teacher_login_path, json={'login': 'invalid', 'password': 'invalid'})
        self.assert404(response)

    def test_incorect_password(self):
        response = self.client.post(teacher_login_path, json={'login': teacher_credentials['login'], 'password': 'invalid'})
        self.assert401(response)

class TestLogoutTeacher(BaseTestCase):
    def setUp(self):
        add_test_university(university_schema)
        add_test_teacher(teacher_schema)

    def test_sucess(self):
        super().auth(teacher_login_path, teacher_credentials)
        response = self.client.get('/teacher/logout', headers=self.auth_header)
        self.assert200(response)
