"""
SQLAlchemy models for the database.
"""
from . import db
from flask_jwt_extended import create_access_token, create_refresh_token
import json
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import ENUM
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        phone_number (str): The phone number of the user.
        email (str): The email address of the user.
        business_name (str): The name of the user's business.
        business_address (str): The address of the user's business.
        business_logo_link (str): The link to the business logo.
        business_id (str): The ID for business identification.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    business_email = db.Column(db.String(100), nullable=True)
    business_phone = db.Column(db.String(15), nullable=False)
    business_type = db.Column(db.Integer, default=0)
    business_logo_link = db.Column(db.String(200))
    business_id = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(225), nullable=False)
    admin_type = db.Column(db.String(45), ENUM("user", "admin"), default="user")
    created = db.Column(db.DateTime, default=func.now())
    block_stat = db.Column(db.Integer, nullable=False, default=0)
    passresetcode = db.Column(db.String(255), nullable=True)
    last_login = db.Column(db.DateTime, default=func.now())
    last_password_reset = db.Column(db.String(50), nullable=True)
    activated = db.Column(db.Integer, default=1)  # default to 0 if using email validation
    activatecode = db.Column(db.String(255), nullable=True)
    last_activation_code_time = db.Column(db.DateTime(), nullable=True)
    customers = db.relationship('Customer', backref='user', lazy=True)

    def __repr__(self):
        """
        Returns a printable representation of the User object.
        """
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

    def encode_auth_token(self, user):
        """
        Generates the Auth Tokens
        :return: dictionary
        """
        try:
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return {'status': 1, 'access_token': access_token, 'refresh_token': refresh_token, 'error': None}
        except Exception as e:
            return {'status': 2, 'access_token': None, 'refresh_token': None, 'error': [str(e)]}

    @classmethod
    def add_user(cls, new_user_info):
        """
        Adds user information to the database.

        Args:
        - username: Username of the user
        - email: Email of the user

        Returns:
        - True if user added successfully, False otherwise
        """
        existing_user = cls.query.filter_by(email=new_user_info['email']).first()
        if existing_user:
            return False, 'User with this username already exists'

        new_user = cls(first_name=new_user_info['first_name'].title(), last_name=new_user_info['last_name'].title(),
                       phone_number=new_user_info['phone'], email=new_user_info['email'],
                       password=generate_password_hash(new_user_info['password']),
                       business_name=new_user_info['business_name'],
                       business_id=new_user_info['business_id'], business_phone=new_user_info['business_phone'],
                       business_email=new_user_info['business_email'])
        db.session.add(new_user)
        db.session.commit()
        return True, 'User added successfully'


class Customer(db.Model):
    """
    Represents a customer in the database.

    Attributes:
        id (int): The unique identifier for the customer.
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        email (str): The email address of the customer.
        phone_number (str): The phone number of the customer.
        shipping_address (str): The shipping address of the customer.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    shipping_address = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='customer', lazy=True)

    def __repr__(self):
        """
        Returns a printable representation of the Customer object.
        """
        return f"Customer('{self.first_name}', '{self.last_name}', '{self.email}')"


class Transaction(db.Model):
    """
    Represents a transaction in the database.

    Attributes:
        id (int): The unique identifier for the transaction.
        order_id (str): The order ID for the transaction.
        product_name (str): The name of the product.
        product_description (str): The description of the product.
        order_date (DateTime): The date of the order.
        delivery_address (str): The delivery address for the order.
        delivery_date (DateTime): The delivery date for the order.
        total_price (float): The total price for the products.
        delivery_fee (float): The delivery fee.
        invoice_link (str): The link to the invoice.
        discount_applied (float): The discount applied.
        amount_paid (float): The amount paid by the customer.
        remaining_balance (float): The remaining balance to be paid.
        due_date (DateTime): The due date for payment.
        payment_status (str): Status of payment (e.g., 'paid', 'partially paid', 'unpaid').
    """

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_id = db.Column(db.String(50), nullable=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.Text)
    order_date = db.Column(db.DateTime, nullable=True)
    delivery_address = db.Column(db.String(200), nullable=False)
    delivery_date = db.Column(db.DateTime)
    total_price = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, nullable=False)
    invoice_link = db.Column(db.String(200))
    receipt_link = db.Column(db.String(200))
    discount_applied = db.Column(db.Float)
    amount_paid = db.Column(db.Float, nullable=True)
    remaining_balance = db.Column(db.Float, nullable=True)
    due_date = db.Column(db.DateTime)
    payment_status = db.Column(db.String(20), nullable=False)  # full,part,none

    def __repr__(self):
        """
        Returns a printable representation of the Transaction object.
        """
        return f"Transaction('{self.order_id}', '{self.product_name}', '{self.order_date}')"


class Settings(db.Model):
    """
    Represents user account preferences in the database.

    Attributes:
        id (int): The unique identifier for the settings.
        user_id (int): The user ID associated with the settings.
        template_mode (str): The chosen template mode ('light' or 'dark').
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    template_mode = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        """
        Returns a printable representation of the Settings object.
        """
        return f"Settings('{self.user_id}', '{self.template_mode}')"


class RevokedTokens(db.Model):
    """
    Model to manage revoked tokens for users.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    token_list = db.Column(db.String(500), default=json.dumps([]))  # Assuming max length for token list

    def __init__(self, user_id):
        """
        Initializes a RevokedTokenModel instance.

        Args:
        - user_id: ID of the user associated with the tokens
        - token_list: List of revoked tokens (JSON-formatted string)
        """
        self.user_id = user_id

    @classmethod
    def add_revoked_token(cls, token):
        """
        Adds a revoked token for a user to the database.

        Args:
        - user_id: ID of the user associated with the token
        - token: Token string to be added to the revoked list
        """
        revoked_token = cls.query.filter_by(user_id=cls.user_id).first()
        tokens = json.loads(revoked_token.token_list)
        tokens.append(token)
        revoked_token.token_list = json.dumps(tokens)
        db.session.commit()
        return

    def get_token_list(self):
        """
        Returns the list of revoked tokens for the user.
        """
        return json.loads(self.token_list) if self.token_list else []

    def is_token_revoked(self, token):
        """
        Checks if a token is revoked for the user.

        Args:
        - token: Token string to be checked for revocation

        Returns:
        - True if the token is revoked for the user, False otherwise
        """
        token_list = json.loads(self.token_list) if self.token_list else []
        return token in token_list
