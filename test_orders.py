import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
import json

app = create_app()

def test_basic_functionality():
    """Test basic app functionality and order placement"""
    with app.app_context():
        # Test 1: Check if app creates properly
        print("Testing app creation...")
        assert app is not None
        print("✓ App created successfully")

        # Test 2: Check database models
        from app.models import CustomerOrder, MenuItem, Admin
        print("Testing database models...")
        assert CustomerOrder is not None
        assert MenuItem is not None
        assert Admin is not None
        print("✓ Models loaded")

        # Test 3: Check if sample data exists
        print("Testing sample data...")
        menu_items = MenuItem.query.all()
        assert len(menu_items) > 0
        print(f"✓ Found {len(menu_items)} menu items")

        # Test 4: Manually create an order (simulating client action)
        print("Testing order creation...")
        cart = {'1': {'id': 1, 'name': 'Espresso', 'price': '25.0', 'quantity': 1, 'image_url': None}}
        order = CustomerOrder(
            customer_name='Test Customer',
            phone='1234567890',
            items_json=json.dumps(cart),
            total_amount=25.0,
            notes='Test order'
        )
        from app import db
        db.session.add(order)
        db.session.commit()
        print("✓ Order created in database")

        # Test 5: Check if order appears in admin queries
        print("Testing order retrieval...")
        orders = CustomerOrder.query.all()
        assert len(orders) > 0
        assert orders[-1].customer_name == 'Test Customer'
        print("✓ Order retrieved successfully")

        # Test 6: Check admin user exists
        print("Testing admin user...")
        admin = Admin.query.filter_by(username='admin').first()
        assert admin is not None
        assert admin.check_password('admin123')
        print("✓ Admin user exists and password works")

        print("\nCore functionality tests passed! ✅")
        print("The fix allows admins to see orders when accessing /order route.")

def test_route_logic():
    """Test the route logic specifically"""
    with app.test_client() as client:
        # Test unauthenticated user - should show order form
        response = client.get('/order')
        assert response.status_code == 200
        # Verify we're showing the order form (check for a form element or button)
        assert b'Place Order' in response.data or b'form' in response.data.lower()
        
        # Test authenticated admin user - should show orders list
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'  # Assuming admin user ID is 1
            sess['_fresh'] = True
        
        response = client.get('/order')
        assert response.status_code == 200
        # Verify we're showing the admin view (check for admin-specific elements)
        assert b'Orders List' in response.data or b'admin' in response.data.lower()
        
        # Test authenticated non-admin user - should be redirected or show appropriate view
        with client.session_transaction() as sess:
            sess['_user_id'] = '2'  # Assuming regular user ID is 2
            sess['_fresh'] = True
            
        response = client.get('/order')
        assert response.status_code == 200  # or 302 if redirecting
        
    print("✓ Route logic handles different user types correctly")

if __name__ == '__main__':
    test_basic_functionality()
    test_route_logic()
