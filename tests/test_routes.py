import unittest
from myapp import app


class TestRoutes(unittest.TestCase):
    """
    Test cases for the routes in the Flask app.

    Attributes:
        app (Flask): The Flask application object used for testing.
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.app = app.test_client()

    def tearDown(self):
        """
        Clean up after each test if needed.
        """
        pass

    def test_test_route(self):
        """
        Test the '/test' route.

        Checks:
            - Status code is 200.
            - Keys 'status', 'data', 'message', 'error' exist in the response data.
        """
        response = self.app.get('/test')
        data = response.get_json()

        # Test if status code is 200
        self.assertEqual(response.status_code, 200)

        # Test if keys exist in the response data
        self.assertIn('status', data)
        self.assertIn('data', data)
        self.assertIn('message', data)
        self.assertIn('error', data)

    def test_user_route(self):
        """
        Test the '/user' route.

        Checks:
            - Status code is 201 for successful user creation.
            - Verify the content of the response JSON.
        """
        # Simulating user data
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "email": "john@example.com",
            "business_name": "Business ABC",
            "business_address": "123 Main St",
            "business_logo_link": "https://example.com/logo",
            "business_id": "ABC123"
            # Include other user information as needed
        }

        response = self.app.post('/user', json=user_data, content_type='application/json')
        data = response.get_json()

        # Test if status code is 201 (created)
        self.assertEqual(response.status_code, 201)

        # Verify the content of the response JSON
        self.assertEqual(data['message'], 'User information saved successfully')

    def test_settings_route(self):
        """
        Test the '/settings' route.

        Checks:
            - Status code is 200 for successful retrieval.
            - Verify the content of the response JSON.
        """
        # Simulating a user ID in the request payload
        user_id = {"user_id": 123}

        response = self.app.post('/settings', json=user_id, content_type='application/json')
        data = response.get_json()

        # Test if status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verify the content of the response JSON
        self.assertIn('user_id', data)
        self.assertIn('template_mode', data)
        # Add assertions for other expected keys/values in the settings response


if __name__ == '__main__':
    unittest.main()
