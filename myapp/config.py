import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'fundsflow.db')

SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRETE_KEY = os.environ.get('SECRETE_KEY')

JWT_SECRET_KEY = os.environ.get('SECRETE_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expires after 1 hour of inactivity
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token validity

CORS_HEADERS = "Content-Type"
