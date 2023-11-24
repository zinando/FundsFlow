from flask import jsonify, request
from myapp import app
from myapp.models import *


@app.route('/test', methods=['GET'])
def test_route():

    """
    Test route to return a dictionary with specific keys.

    Returns:
        JSON response with a dictionary containing status, data, message, and error keys.
    """
    # Example data for demonstration purposes
    response_data = {
        'status': 1,
        'data': {'key1': 'value1', 'key2': 'value2'},
        'message': 'Backend accessed successfully',
        'error': None
    }

    return jsonify(response_data)

@app.route('/settings', methods=['POST'])
def get_user_settings():
    """
    Retrieve user settings as a dictionary.

    Request Payload Format:
    {
        "user_id": 123  # Replace with actual user ID
    }

    Returns:
        JSON response containing user settings.
    """
    request_data = request.get_json()
    user_id = request_data.get('user_id')

    if user_id:
        user_settings = Settings.query.filter_by(user_id=user_id).first()

        if user_settings:
            settings_dict = {
                'user_id': user_settings.user_id,
                'template_mode': user_settings.template_mode
                # Add other settings if needed
            }
            return jsonify(settings_dict), 200
        else:
            return jsonify({'message': 'Settings not found for the user'}), 404
    else:
        return jsonify({'message': 'User ID not provided in request payload'}), 400


@app.route('/user', methods=['POST'])
def save_user_info():

    """
    Save user information into the User table.

    Request Payload Format:
    {
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

    Returns:
        JSON response with a success message.
    """
    user_data = request.get_json()

    new_user = User(
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        phone_number=user_data.get('phone_number'),
        email=user_data.get('email'),
        business_name=user_data.get('business_name'),
        business_address=user_data.get('business_address'),
        business_logo_link=user_data.get('business_logo_link'),
        business_id=user_data.get('business_id')
        # Map other user data attributes as needed
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User information saved successfully'}), 201
