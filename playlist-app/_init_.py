# playlist_app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Create the database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Change to persistent database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

    # Initialize extensions
    db.init_app(app)  
    migrate = Migrate(app, db)

    return app
