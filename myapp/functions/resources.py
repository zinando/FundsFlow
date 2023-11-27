from myapp.functions import myfunctions as myfunc
from myapp.models import User, Customer, Transaction


def generate_business_id(business_name: str) -> str:
    """ attaches a random 4-digit code to surname to form userid
        ensures userid is unique
    """

    def generate_random_code():
        """generates random code of 4-digits numbers and attaches it to the first-four letters of the business name"""
        code = myfunc.random_numbers(4)
        userid = "{}_{}".format(business_name.lower()[3:], code)
        if User.query.filter_by(business_id=userid).count() > 0:
            generate_random_code()
        return userid

    return generate_random_code()


def fetch_user_info(user_id: int) -> dict:
    """
    Fetches user information from the database based on the provided user ID.

    Args:
        user_id (int): The ID of the user whose information is to be fetched.

    Returns:
        dict : A dictionary containing user information if the user exists in the database.
                      Returns empty dict if the user does not exist.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return {}

    mr = {'user_id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'phone': user.phone_number,
          'email': user.email, 'business_name': user.business_name, 'business_phone': user.business_phone,
          'business_email': user.business_email, 'blocked_status': user.blockstat, 'activated': user.activated,
          'business_type': user.business_type, 'logo': user.business_logo_link, 'admin_type': user.admin_type,
          'business_id': user.business_id, 'customers': []}

    return mr


def fetch_customer_info(user_id, customer_id=None):
    """
    Fetches customer information based on user_id and optionally customer_id.

    Args:
        user_id (int): The user ID associated with the customers.
        customer_id (int, optional): The customer ID to fetch information for (default: None).

    Returns:
        dict or list of dict: A dictionary of customer information if customer_id is provided.
                              If customer_id is None, returns a list of dictionaries containing
                              information of all customers associated with the user_id.

    Raises:
        ValueError: If user_id is not provided.
    """
    if user_id is None:
        raise ValueError("User ID must be provided.")

    if customer_id is not None:
        # Fetch info for a specific customer
        customer = Customer.query.filter_by(user_id=user_id, id=customer_id).first()
        if customer:
            return {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone_number': customer.phone_number,
                'shipping_address': customer.shipping_address,
                'user_id': customer.user_id
            }
        else:
            return {}

    else:
        # Fetch info for all customers associated with the user_id
        customers = Customer.query.filter_by(user_id=user_id).all()
        customers_info = []
        for customer in customers:
            customer_info = {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone_number': customer.phone_number,
                'shipping_address': customer.shipping_address,
                'user_id': customer.user_id
            }
            customers_info.append(customer_info)

        return customers_info


def fetch_customer_transactions(customer_id):
    """
    Fetches all transaction instances associated with a given customer ID.

    Args:
        customer_id (int): The ID of the customer.

    Returns:
        list of dict: A list of dictionaries containing information of all transactions
                      associated with the provided customer_id.
    """
    transactions = Transaction.query.filter_by(customer_id=customer_id).all()
    transactions_info = []

    date_format = '%Y-%m-%d %H:%M:%S'  # Change this format based on your preference

    for transaction in transactions:
        transaction_info = {
            'transaction_id': transaction.id,
            'customer_id': transaction.customer_id,
            'order_id': transaction.order_id,
            'product_name': transaction.product_name,
            'product_description': transaction.product_description,
            'order_date': transaction.order_date.strftime(date_format) if transaction.order_date else None,
            'delivery_address': transaction.delivery_address,
            'delivery_date': transaction.delivery_date.strftime(date_format) if transaction.delivery_date else None,
            'rate': transaction.rate,
            'quantity': transaction.quantity,
            'discount_applied': transaction.discount_applied,
            'total_price': transaction.total_price,
            'delivery_fee': transaction.delivery_fee,
            'invoice_link': transaction.invoice_link,
            'receipt_link': transaction.receipt_link,
            'amount_paid': transaction.amount_paid,
            'remaining_balance': transaction.remaining_balance,
            'due_date': transaction.due_date.strftime(date_format) if transaction.due_date else None,
            'payment_status': transaction.payment_status
        }
        transactions_info.append(transaction_info)

    return transactions_info

