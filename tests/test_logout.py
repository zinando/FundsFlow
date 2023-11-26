import unittest
from flask import json
from myapp import app, db
from myapp.models import User

class TestLogoutRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

        # Create a test user for logout testing
        # Example: Create a User in the test database
        test_user = User(email='test@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()

        # Simulate a login for the test user to obtain an access token
        login_data = {
            'email': 'test@example.com',
            'password': 'password'
        }
        response = self.app.post('/login', json=login_data)
        self.access_token = json.loads(response.data.decode())['data']['access_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_logout(self):
        # Test logout with a valid access token
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.app.delete('/logout', headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 1)
        # Add assertions for successful logout

    def test_unauthorized_logout(self):
        # Test logout without providing an access token
        response = self.app.delete('/logout')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 2)
        # Add assertions for unauthorized logout due to missing token

    # Add more test cases for different scenarios (e.g., expired token, invalid token, etc.)

if __name__ == '__main__':
    unittest.main()
