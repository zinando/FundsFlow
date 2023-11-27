from flask import jsonify, request
from myapp import app, db, jwt
from myapp.models import *
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, current_user, get_jwt
)
import json
from datetime import datetime
from myapp.functions import myfunctions as myfunc
from werkzeug.security import check_password_hash
from myapp.functions import resources as resource


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token has expired. User need to login to continue browsing this site.",
                "error": "fresh token is required",
            }
        ),
        401,
    )


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(userid=identity).one_or_none()


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    err = 'authentication token has expired.'
    message = 'User could not be authenticated. Pleas login again!'
    return json.dumps({'status': 2, 'data': None, 'message': message, 'error': [err]}), 401


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    message = 'Access token refreshed successfully'
    return json.dumps({'status': 1, 'data': {'access_token': new_access_token},
                       'message': message, 'error': [None]}), 200


@app.route('/', methods=['GET', 'POST'])
def index():
    return json.dumps({'status': 1, 'data': None, 'message': 'Connection successful.', 'error': [None]})


@app.route('/test', methods=['GET'])
def test_route():
    """
    Test route to return a dictionary with specific keys.

    Returns:
        JSON response with a dictionary containing status, data, message, and error keys.
    """
    # db.create_all()
    # Example data for demonstration purposes
    response_data = {
        'status': 1,
        'data': {'key1': 'value1', 'key2': 'value2'},
        'message': 'FundsFlow Backend accessed successfully',
        'error': None
    }

    return jsonify(response_data)


@app.route("/signup", methods=["POST"])
def signup() -> str:
    """ receives sign up request and converts the data into python dict then returns a response """

    data = request.get_json()
    action = request.args.get('action')
    if action == 'SIGNUP-USER':
        if 'password' in data and 'email' in data:
            password = data['password']
            # validate password strength
            check_password = myfunc.check_password_strength(password)
            if check_password['status'] > 1:
                return json.dumps(check_password)

            # register user
            users = User()
            user_is_registered, message = users.add_user(data)
            if user_is_registered:
                user = User.query.filter_by(email=data['email']).first()
                worker = {'email': user.email, 'user_id': user.id}
                return json.dumps({'status': 1, 'data': worker, 'message': message, 'error': [None]})
            else:
                return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

        message = 'user parameters not recognised.'
        return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

    elif action == 'REGISTER-USER-PERSONAL-INFORMATION':
        if 'user_id' in data:
            user = User.query.filter_by(id=data['user_id']).first()
            if user:
                User.query.filter_by(id=data['user_id']) \
                    .update({'first_name': data['first_name'].title(),
                             'last_name': data['last_name'].title(),
                             'phone_number': data['phone']})
                db.session.commit()
                status = 1
                # fetch the saved user-data
                user = User.query.filter_by(id=data['user_id']).first()
                worker = {'email': user.email, 'user_id': user.id, 'phone': user.phone_number,
                          'first_name': user.first_name, 'last_name': user.last_name}
                message = 'User personal info updated successfully'

            else:
                status = 2
                message = 'User not found'
                worker = None

            return json.dumps({'status': status, 'data': worker, 'message': message, 'error': [message]})

        message = 'No user id provided'
        return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

    elif action == 'REGISTER-USER-BUSINESS-INFORMATION':
        if 'user_id' in data and 'business_name' in data:
            # generate business id for user
            data['business_id'] = resource.generate_business_id(data['business_name'])

            user = User.query.filter_by(id=data['user_id']).first()
            if user:
                User.query.filter_by(id=data['user_id']) \
                    .update({'business_name': data['business_name'],
                             'business_phone': data['business_phone'] if data['business_phone'] else user.phone_number,
                             'business_email': data['business_email'] if data['business_email'] else user.email,
                             'business_type': data['business_type'], 'business_id': data['business_id']})
                db.session.commit()
                status = 1
                # fetch the saved user-data
                user = User.query.filter_by(id=data['user_id']).first()
                worker = resource.fetch_user_information(user.id)
                message = 'User business info updated successfully'

            else:
                status = 2
                message = 'User not found'
                worker = None

            return json.dumps({'status': status, 'data': worker, 'message': message, 'error': [message]})

        message = 'No user id and or business name provided'
        return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

    message = 'No action defined'
    return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})


@app.route("/login", methods=["POST"])
def login() -> str:
    """ receives login request and converts the data into python dict then returns a response """
    data = request.get_json()

    if 'email' in data and 'password' in data:
        email, password = data['email'], data['password']
        user = User.query.filter_by(email=email).first()
        # check if user exists
        if not user:
            message = 'User does not exist.'
            return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

        # check if password matches
        if not check_password_hash(user.password, password):
            message = 'Password is incorrect.'
            return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

        # check if user is active
        if not User.query.filter_by(email=email, activated=1).first():
            message = 'User has not confirmed their email'
            return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

        # check if user is blocked
        if not User.query.filter_by(email=email, block_stat=0).first():
            message = 'Account is blocked. Pleased contact admin.'
            return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

        # log user in
        response = user.encode_auth_token(user)
        if response['status'] == 1:
            worker = resource.fetch_user_information(user.id)
            worker['access_token'] = response['access_token']
            worker['refresh_token'] = response['refresh_token']
            message = 'Login was successful.'
            return json.dumps({'status': 1, 'data': worker, 'message': message, 'error': [None]})

        # else
        message = 'Login was not successful.'
        return json.dumps({'status': 2, 'data': data, 'message': message, 'error': response['error']})

    message = 'user parameters not recognised.'
    return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    worker = RevokedToken(current_user.id)
    worker.add_revoked_token(jti)
    return json.dumps({'status': 1, 'data': None, 'message': 'Logged out successfully.', 'error': [None]})


@app.route('/customer', methods=['POST'])
@jwt_required()
def customer():
    data = request.get_json()
    action = request.args.get('action')
    if action == 'ADD-CUSTOMER' and 'first_name' in data:
        new_customer = Customer(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            shipping_address=data['shipping_address'],
            user_id=current_user.id
        )

        db.session.add(new_customer)
        db.session.commit()
        message = 'Customer added successfully'
        worker = resource.fetch_customer_info(current_user.id, new_customer.id)

        return json.dumps({'status': 1, 'data': worker, 'message': message, 'error': [None]})

    elif action == 'FETCH-CUSTOMERS':
        worker = resource.fetch_customer_info(current_user.id)
        return json.dumps({'status': 1, 'data': worker, 'message': 'Succeeded.', 'error': [None]})

    elif action == 'FETCH-CUSTOMER-TRANSACTIONS' and 'customer_id' in data:
        worker = resource.fetch_customer_transactions(data['customer_id'])

        return json.dumps({'status': 1, 'data': worker, 'message': 'Succeeded', 'error': [None]})

    message = 'Invalid request action argument or no valid resource parameter in request data'
    return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})


@app.route('/transactions', methods=['POST'])
@jwt_required()
def transaction():
    data = request.get_json()
    action = request.args.get('action')

    if action == 'LOG-TRANSACTION' and 'customer_id' in data:  # logging generated invoice data
        amount_payable = data['total_price'] + data['delivery_fee'] - data['discount']
        remaining_balance = amount_payable - data['amount_paid'] if data['amount_paid'] else amount_payable
        new_transaction = Transaction(
            customer_id=data['customer_id'],
            product_name=data['product_name'],
            product_description=data['product_description'],
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d %H:%M:%S') if data['order_date'] else None,
            delivery_address=data['delivery_address'],
            delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%d %H:%M:%S') if data[
                'delivery_date'] else None,
            number_of_items=data['number_of_items'],
            discount_applied=data['discount'],
            total_price=data['total_price'],
            delivery_fee=data['delivery_fee'],
            amount_payable=amount_payable,
            invoice_link=data['invoice_link'],
            receipt_link=data['receipt_link'],
            amount_paid=data['amount_paid'] if data['amount_paid'] else 0,
            remaining_balance=remaining_balance,
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d %H:%M:%S') if data['due_date'] else None,
            payment_status='paid' if remaining_balance == 0 else 'pending'
        )

        db.session.add(new_transaction)
        db.session.commit()

        worker = resource.fetch_customer_transactions(data['customer_id'])

        return json.dumps({'status': 1, 'data': worker, 'message': 'Transaction Logged successfully.', 'error': [None]})

    elif action == 'UPDATE-TRANSACTION-INFO' and 'transaction_id' in data and 'customer_id' in data:
        trans_info = Transaction.query.filter_by(id=data['transaction_id']).first()
        if trans_info:
            total_paid = trans_info.amount_paid + data['amount_paid']
            remaining_balance = trans_info.amount_payable - total_paid
            status = 'paid' if remaining_balance == 0 else 'pending'
            Transaction.query.filter_by(id=data['transaction_id']) \
                .update({'amount_paid': total_paid,
                         'remaining_balance': remaining_balance,
                         'payment_status': status})
            db.session.commit()

            worker = resource.fetch_customer_transactions(data['customer_id'])

            return json.dumps(
                {'status': 1, 'data': worker, 'message': 'Transaction updated successfully.', 'error': [None]})

        message = 'record not found'
        return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

    elif action == 'DELETE-TRANSACTION' and 'transaction_id' in data and 'customer_id' in data:
        trans_info = Transaction.query.filter_by(id=data['transaction_id']).first()
        if trans_info:
            Transaction.query.filter_by(id=data['transaction_id']).delete()
            db.session.commit()

            worker = resource.fetch_customer_transactions(data['customer_id'])

            return json.dumps(
                {'status': 1, 'data': worker, 'message': 'Transaction deleted successfully.', 'error': [None]})

        message = 'Transaction record not found'
        return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})

    message = 'Invalid request action argument or no valid resource parameter in request data'
    return json.dumps({'status': 2, 'data': data, 'message': message, 'error': [message]})


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
