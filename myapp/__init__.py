from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
migrate = Migrate(app, db)
jwt = JWTManager(app)

"""
Initialize the Flask app.

Attributes:
    app (Flask): The Flask application object.
    db (SQLAlchemy): The SQLAlchemy database object.
"""

# Import routes after db initialization
from myapp import routes

