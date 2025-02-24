import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure app using environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_name = 'sqlite:///' + os.path.join(basedir, 'bietapp.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Bootstrap(app)

    # Register Blueprints
    from .routes import main_app
    app.register_blueprint(main_app)

    return app

auth = HTTPBasicAuth()

# Users and passwords for basic authentication
users = {
    "fabi": generate_password_hash("control"),
    "admin": generate_password_hash("lookup")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
