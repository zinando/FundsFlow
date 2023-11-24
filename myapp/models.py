"""
SQLAlchemy models for the database.
"""
from myapp import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


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
    business_address = db.Column(db.String(200), nullable=True)
    business_logo_link = db.Column(db.String(200))
    business_id = db.Column(db.String(50), unique=True, nullable=True)
    customers = db.relationship('Customer', backref='user', lazy=True)

    def __repr__(self):
        """
        Returns a printable representation of the User object.
        """
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"


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
    payment_status = db.Column(db.String(20), nullable=False) #full,part,none

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


