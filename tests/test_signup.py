import sys
sys.path.append('C:\\Users\\user\\Documents\\GitHub\\Projects\\FundsFlow')
import unittest
from flask import json
from myapp import app, db


class TestSignupRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        # Create the application context
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_signup(self):
        """Test successful user signup"""

        # Data for successful signup
        data = {
            'password': 'YOUAREmad2#',
            'business_name': 'JonDoe',
            'first_name': "Jon",
            'last_name': 'Doe',
            'phone': '07031104270',
            'email': 'jon_doe@yahoo.com',
            'business_address': '20 Wale street'
            # Add other required fields for signup
        }

        response = self.app.post('/signup', json=data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 1)
        self.assertIsNotNone(data['data']['business_id'])
        # Add more assertions for successful signup

    def test_signup_missing_fields(self):
        """Test signup with missing fields"""

        # Data with missing required fields
        invalid_data = {
            # Missing required fields for signup
        }

        response = self.app.post('/signup', json=invalid_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 2)
        # Add assertions for unsuccessful signup due to missing data


if __name__ == '__main__':
    unittest.main()
