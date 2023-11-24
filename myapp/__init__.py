from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fundsflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRETE_KEY')

"""
Initialize the Flask app.

Attributes:
    app (Flask): The Flask application object.
    db (SQLAlchemy): The SQLAlchemy database object.
"""

# Import routes after db initialization
from myapp import routes

