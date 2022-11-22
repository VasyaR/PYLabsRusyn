from app.models import *
from tests.base_test_case import BaseTestCase
from tests.test_data_generator import *
import copy

class TestAddUniversity(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/', json=university_schema, headers=self.auth_header)
        self.assert200(response)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, admin2_credentials)
        response = self.client.post('/university/', json=university_schema)
        self.assert401(response)

    def test_invalid_already_exists(self):
        add_test_university(university_schema)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/', json=university_schema, headers=self.auth_header)
        self.assert400(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/university/', json=university_schema, headers=self.auth_header)
        self.assert403(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

class TestGetUniversities(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.get('/university/', headers=self.auth_header)
        should_be = copy.deepcopy(university_schema)
        should_be['id'] = 1
        self.assert200(response)
        self.assertEqual(response.json, [should_be])

class TestUpdateUniversity(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/1', json=university_schema, headers=self.auth_header)
        self.assertStatus(response, 201)

    def test_invalid_no_credentials(self):
        response = self.client.post('/university/1', json=university_schema)
        self.assert401(response)

    def test_invalid_no_data(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/1', json=None, headers=self.auth_header)
        self.assert400(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/university/1', json=university_schema, headers=self.auth_header)
        self.assert403(response)

    def test_bad_request(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/1', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

    def test_invalid_id(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/university/2', json=university_schema, headers=self.auth_header)
        self.assert404(response)

class TestDeleteUniversity(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)
        add_test_university(university_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/university/1', headers=self.auth_header)
        self.assertStatus(response, 204)

    def test_invalid_no_credentials(self):
        response = self.client.delete('/university/1')
        self.assert401(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.delete('/university/1', headers=self.auth_header)
        self.assert403(response)

    def test_invalid_id(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/university/2', headers=self.auth_header)
        self.assert404(response)

