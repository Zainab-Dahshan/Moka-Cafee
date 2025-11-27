from app import create_app, db
from app.models import Admin, MenuItem
import os

def create_admin():
    # Check if admin user exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        # Create admin user
        admin = Admin(username='admin')
        admin.set_password('admin123')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")

def create_sample_data():
    # Add some sample menu items if none exist
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
                description='Light and refreshing green tea leaves.',
                price=20.0,
                category='Tea',
                image_url=None,
                is_available=True
            ),
            MenuItem(
                name='Chocolate Cake',
                description='Rich and moist chocolate cake with chocolate frosting.',
                price=35.0,
                category='Dessert',
                image_url=None,
                is_available=True
            )
        ]
        
        db.session.bulk_save_objects(sample_items)
        db.session.commit()
        print("Sample menu items created!")

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Admin': Admin,
        'MenuItem': MenuItem,
        'CustomerOrder': CustomerOrder
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
        create_sample_data()
    
    # Create necessary directories if they don't exist
    os.makedirs(os.path.join(app.root_path, 'static/images/products'), exist_ok=True)
    
    # Run the application
    app.run(host='0.0.0.0', port=8000, debug=False)
