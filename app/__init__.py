from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
    app.config['UPLOAD_FOLDER'] = 'static/images/products'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    # Ensure upload folder exists
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    
    # Register blueprints
    from .routes import main, admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
