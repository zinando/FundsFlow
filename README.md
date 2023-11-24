# FundsFlow

FundsFlow is a React-based web application that aids business owners in managing their finances electronically. It provides tools to generate invoices for orders, send payment receipts, and track payment history seamlessly.

## Features

- **Invoice Generation:** Create and manage invoices for orders.
- **Payment Receipts:** Automatically send receipts upon payment completion.
- **Payment History:** Track and manage payment history for financial insights.

## Technologies Used

- **Frontend:** React.js
- **Backend:** Python Flask
- **Database:** SQLAlchemy with SQLite

## Installation

### Prerequisites

- Node.js
- Python 3
- SQLite

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FundsFlow.git
   ```
2. Navigate to the backend directory and set up the Flask environment (assuming you have a virtual environment):
   ```bash
   cd FundsFlow/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the Flask backend (ensure the virtual environment is activated):
   ```bash
   flask run
   ```
4. Run the React frontend:
   ```bash
   cd FundsFlow/frontend
   npm start
   ```


## Usage

- **Login/Authentication:** Users can sign up or log in to the platform using their email and password.
- **Invoice Generation:** To create an invoice, navigate to the 'Invoices' section, click on 'New Invoice', fill in the details, and save.
- **Payment History:** Access the 'Payments' or 'Transaction History' section to view and analyze payment history.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Add credits or acknowledgements to any contributors, libraries, or resources used.


