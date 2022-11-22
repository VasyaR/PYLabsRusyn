from app.models import *
from tests.base_test_case import BaseTestCase
from tests.test_data_generator import *

invalid_credentials = {
    'login': 'admin',
    'password': 'none'
}

class TestAdminAuth(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)

    def test_success(self):
        response = self.client.post(admin_login_path, json=admin_credentials)
        self.assert200(response)
        self.assertTrue('token' in response.json)
    
    def test_invalid_login(self):
        credentials_invalid_login = {
            'login': 'admin1',
            'password': 'admin'
        }
        response = self.client.post('/admin/login', json=credentials_invalid_login)
        self.assertEqual(response.status_code, 404)

    def test_invalid_password(self):
        credentials_invalid_login = {
            'login': 'admin',
            'password': 'admin1'
        }
        response = self.client.post('/admin/login', json=credentials_invalid_login)
        self.assert401(response)

    def test_invalid_request(self):
        response = self.client.post('/admin/login', json={'invaid': 'request'})
        self.assert400(response)

    def test_no_data(self):
        response = self.client.post('/admin/login', json={})
        self.assert400(response)

class TestAdminDelete(BaseTestCase):
    def setUp(self):
        add_test_admin(admin_schema)

    def test_success(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/admin/1', headers=self.auth_header)
        self.assertStatus(response, 204)

    def test_invalid_no_credentials(self):
        super().auth(admin_login_path, invalid_credentials)
        response = self.client.delete('/admin/1', headers=self.auth_header)
        self.assert401(response)

    def test_invalid_wrong_id(self):
        super().auth(admin_login_path, admin_credentials)
        response = self.client.delete('/admin/2', headers=self.auth_header)
        self.assert404(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.delete('/admin/1', headers=self.auth_header)
        self.assert403(response)

class TestAddAdmin(BaseTestCase):
    def test_success(self):
        add_test_admin(admin_credentials)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/admin/', json=admin2_schema, headers=self.auth_header)
        self.assert200(response)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/admin/', json=admin2_schema, headers=self.auth_header)
        self.assert403(response)

    def test_bad_request(self):    
        add_test_admin(admin_credentials)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/admin/', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

    def test_already_exists(self):
        add_test_admin(admin_credentials)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/admin/', json=admin_schema, headers=self.auth_header)
        self.assert400(response)


class TestUpdateAdmin(BaseTestCase):
    def test_success(self):
        add_test_admin(admin_credentials)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/admin/1', json={'password':'password'}, headers=self.auth_header)
        self.assertStatus(response, 201)

    def test_no_permissions(self):
        add_test_student(student_schema)
        super().auth(student_login_path, student_credentials)
        response = self.client.post('/admin/1', json={'password':'password'}, headers=self.auth_header)
        self.assert403(response)

    def test_bad_request(self):
        add_test_admin(admin_credentials)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/admin/1', json={'bad': 'request'}, headers=self.auth_header)
        self.assert400(response)

    def test_was_not_found(self):
        add_test_admin(admin_credentials)
        super().auth(admin_login_path, admin_credentials)
        response = self.client.post('/admin/2', json={'password':'password'}, headers=self.auth_header)
        self.assert404(response)


