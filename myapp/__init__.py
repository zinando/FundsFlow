from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = "Content-Type"
migrate = Migrate(app, db)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

"""
Initialize the Flask app.

Attributes:
    app (Flask): The Flask application object.
    db (SQLAlchemy): The SQLAlchemy database object.
"""

# Import routes after db initialization
from myapp import routes

