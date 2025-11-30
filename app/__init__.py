from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    app = Flask(__name__, static_folder=static_path)

    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['UPLOAD_FOLDER'] = 'static/images'

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

    # Create database tables and sample data
    with app.app_context():
        db.create_all()
        create_admin()
        create_sample_data()

    return app

def create_admin():
    from .models import Admin
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")

def create_sample_data():
    from .models import MenuItem
    if MenuItem.query.count() == 0:
        sample_items = [
            MenuItem(
                name='Espresso',
                description='Strong black coffee made by forcing steam through ground coffee beans.',
                price=25.0,
                category='Coffee',
                image_url=None,
                is_available=True
            ),
            MenuItem(
                name='Cappuccino',
                description='Espresso with hot milk and steamed milk foam.',
                price=30.0,
                category='Coffee',
                image_url=None,
                is_available=True
            ),
            MenuItem(
                name='Green Tea',
                description='Light and refreshing green tea.',
                price=20.0,
                category='Tea',
                image_url=None,
                is_available=True
            ),
            MenuItem(
                name='Chocolate Cake',
                description='Rich chocolate cake.',
                price=35.0,
                category='Dessert',
                image_url=None,
                is_available=True
            )
        ]

        db.session.bulk_save_objects(sample_items)
        db.session.commit()
        print("Sample menu items created!")
