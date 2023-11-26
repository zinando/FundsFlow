import sys
sys.path.append('C:\\Users\\user\\Documents\\GitHub\\Projects\\FundsFlow')
import unittest
from flask import json
from myapp import app, db


class TestLoginRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        # Create the application context
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        # Create a test user for login testing
        # Example: Create a User in the test database
        # Replace this with actual code to create a test user in your application
        from myapp.models import User
        test_user = User(email='test@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_login(self):
        # Test login with correct credentials
        login_data = {
            'email': 'test@example.com',  # Use the test user's email
            'password': 'password'  # Use the test user's password
        }

        response = self.app.post('/login', json=login_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 1)
        self.assertIsNotNone(data['data']['access_token'])
        # Add more assertions for successful login

    def test_invalid_credentials(self):
        # Test login with incorrect credentials
        invalid_login_data = {
            'email': 'test@example.com',  # Use the test user's email
            'password': 'wrong_password'  # Use an incorrect password
        }

        response = self.app.post('/login', json=invalid_login_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 2)
        # Add assertions for unsuccessful login due to incorrect credentials

    # Add more test cases for different scenarios (e.g., missing fields, inactive user, etc.)


if __name__ == '__main__':
    unittest.main()
