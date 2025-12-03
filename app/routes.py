from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_login import login_required, current_user, login_user, logout_user
from . import db, csrf
from .models import MenuItem, CustomerOrder, Admin, ContactMessage
from .forms import LoginForm, MenuItemForm, OrderForm
import json
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Create blueprint
main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

# Utility function to save uploaded files
def save_uploaded_file(file, upload_folder):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f"images/products/{filename}"
    return None

# Main site routes
@main.route('/')
def index():
    featured_items = MenuItem.query.filter_by(is_available=True).limit(4).all()
    return render_template('index.html', featured_items=featured_items)

@main.route('/menu')
def menu():
    category = request.args.get('category')
    if category:
        items = MenuItem.query.filter_by(category=category, is_available=True).all()
    else:
        items = MenuItem.query.filter_by(is_available=True).all()
    return render_template('menu.html', items=items, category=category)

@main.route('/order', methods=['GET', 'POST'])
def order():
    if current_user.is_authenticated:
        # Show only pending customer orders that need attention
        orders = CustomerOrder.query.filter_by(status='pending').order_by(CustomerOrder.created_at.desc()).all()
        for order in orders:
            order.parsed_items = json.loads(order.items_json)
        return render_template('order.html', orders=orders)

    form = OrderForm()
    cart = session.get('cart', {})

    if form.validate_on_submit():
        # Process the order
        order = CustomerOrder(
            customer_name=form.name.data,
            phone=form.phone.data,
            items_json=json.dumps(cart),
            total_amount=sum(float(item['price']) * item['quantity'] for item in cart.values()),
            notes=form.notes.data
        )
        db.session.add(order)
        db.session.commit()

        # Clear the cart
        session.pop('cart', None)

        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('main.order'))

    return render_template('order.html', form=form, cart=cart)

# Cart management
@main.route('/add_to_cart/<int:item_id>', methods=['POST'])
@csrf.exempt  # Temporarily disable CSRF for testing
def add_to_cart(item_id):
    try:
        item = MenuItem.query.get_or_404(item_id)
        cart = session.get('cart', {})
        
        if str(item_id) in cart:
            cart[str(item_id)]['quantity'] += 1
        else:
            cart[str(item_id)] = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'quantity': 1,
                'image_url': item.image_url or ''
            }
        
        session['cart'] = cart
        
        return jsonify({
            'success': True,
            'cart_count': sum(item['quantity'] for item in cart.values()),
            'message': 'Item added to cart successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding item to cart: {str(e)}'
        }), 400

@main.route('/get_cart')
def get_cart():
    cart = session.get('cart', {})
    # Get the full menu item details for each item in the cart
    cart_with_details = {}
    for item_id, item in cart.items():
        menu_item = MenuItem.query.get(item_id)
        if menu_item:
            cart_with_details[item_id] = {
                'id': menu_item.id,
                'name': menu_item.name,
                'price': str(menu_item.price),
                'quantity': item.get('quantity', 1),
                'image_url': menu_item.image_url
            }
    return jsonify(cart_with_details)

@main.route('/update_cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 1))

    if str(item_id) in cart:
        if quantity <= 0:
            cart.pop(str(item_id))
        else:
            cart[str(item_id)]['quantity'] = quantity

    session['cart'] = cart
    return jsonify({
        'success': True,
        'cart_count': sum(item['quantity'] for item in cart.values())
    })


# Contact routes
@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    contact_msg = ContactMessage(name=name, email=email, message=message)
    db.session.add(contact_msg)
    db.session.commit()

    flash('Your message has been sent successfully!', 'success')
    return redirect(url_for('main.contact'))

# Admin routes
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Login attempt for username: {form.username.data}")  # Debug log
        admin = Admin.query.filter_by(username=form.username.data).first()
        
        if admin:
            print(f"Admin found: {admin.username}")  # Debug log
            if admin.check_password(form.password.data):
                print("Password check passed")  # Debug log
                login_user(admin)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin.dashboard'))
            else:
                print("Password check failed")  # Debug log
        else:
            print("No admin found with that username")  # Debug log
            
        flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@admin.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_products': MenuItem.query.count(),
        'total_orders': CustomerOrder.query.count(),
        'pending_orders': CustomerOrder.query.filter_by(status='pending').count(),
        'all_orders': CustomerOrder.query.order_by(CustomerOrder.created_at.desc()).all()
    }
    for order in stats['all_orders']:
        parsed_items = json.loads(order.items_json)
        # Ensure price is float in the parsed items
        for item_id, item in parsed_items.items():
            if 'price' in item:
                item['price'] = float(item['price'])
        order.parsed_items = parsed_items
    return render_template('admin/Dashboard.html', stats=stats)

@admin.route('/manage', methods=['GET', 'POST'])
@login_required
def manage_items():
    form = MenuItemForm()
    
    if form.validate_on_submit():
        # Handle file upload
        image_url = None
        if 'image' in request.files and request.files['image'].filename != '':
            image_url = save_uploaded_file(
                request.files['image'],
                os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            )
        
        # Create new menu item
        item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            image_url=image_url,
            is_available=form.is_available.data
        )
        
        db.session.add(item)
        db.session.commit()
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin.manage_items'))
    
    items = MenuItem.query.all()
    return render_template('admin/manage_menu.html', form=form, items=items)

@admin.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    form = MenuItemForm(obj=item)
    
    if form.validate_on_submit():
        # Handle file upload
        if 'image' in request.files and request.files['image'].filename != '':
            # Delete old image if exists
            if item.image_url:
                old_image = os.path.join(current_app.root_path, 'static', item.image_url)
                if os.path.exists(old_image):
                    os.remove(old_image)
            
            # Save new image
            item.image_url = save_uploaded_file(
                request.files['image'],
                os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            )
        
        # Update item details
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.category = form.category.data
        item.is_available = form.is_available.data
        
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin.manage_items'))
    
    return render_template('admin/edit_item.html', form=form, item=item)

@admin.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)

    # Delete associated image if exists
    if item.image_url:
        image_path = os.path.join(current_app.root_path, 'static', item.image_url)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(item)
    db.session.commit()

    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('admin.manage_items'))

@admin.route('/orders')
@login_required
def orders():
    orders = CustomerOrder.query.order_by(CustomerOrder.created_at.desc()).all()
    for order in orders:
        order.parsed_items = json.loads(order.items_json)
    return render_template('admin/orders.html', orders=orders)

@admin.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = CustomerOrder.query.get_or_404(order_id)
    new_status = request.form.get('status')

    status_messages = {
        'pending': f'Order #{order_id} is now pending and will be processed soon.',
        'processing': f'Order #{order_id} is now being prepared.',
        'completed': f'Order #{order_id} has been completed successfully.',
        'cancelled': f'Order #{order_id} has been cancelled.'
    }

    if new_status in status_messages:
        order.status = new_status
        db.session.commit()
        flash(status_messages[new_status], 'success')
    else:
        flash('Invalid status', 'danger')

    return redirect(url_for('admin.orders'))
