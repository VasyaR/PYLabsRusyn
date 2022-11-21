from app import db
from flask_testing import TestCase
from app import app

class BaseTestCase(TestCase):
    def auth(self, path, credentials):
        response = self.client.post(path, json=credentials)
        if response.json is not None and 'token' in response.json: 
            self.token = response.json['token']
            self.auth_header = {'Authorization': 'Bearer {0}'.format(self.token)}
        else:
            self.token = None
            self.auth_header = None

    def create_app(self):
        return app

    def tearDown(self):
        db.db_session.rollback()
         
        db.metadata.drop_all(db.engine)
        db.metadata.create_all(db.engine)

