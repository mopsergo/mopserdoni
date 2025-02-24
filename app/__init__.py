from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_httpauth import HTTPBasicAuth
import os

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '1231231241234')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    CSRFProtect(app)

    from .user import user_bp
    from .admin import admin_bp

    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Push application context to perform database operations
    with app.app_context():
        db.create_all()  # Create tables for all models
        add_default_project_needs()  # Add default project needs if necessary

    return app

def add_default_project_needs():
    from .models import ProjectNeed  # Import here to avoid circular import issues

    if ProjectNeed.query.count() == 0:
        default_needs = [
            ProjectNeed(name='Solawi Donihof', saison='25/26', offers_needed = 50, avg_offer_veg=100, avg_offer_bread=15, avg_working_days=5),
        ]
        db.session.bulk_save_objects(default_needs)
        db.session.commit()
