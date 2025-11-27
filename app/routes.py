from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user, login_user, logout_user
from . import db
from .models import MenuItem, CustomerOrder, Admin
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
def add_to_cart(item_id):
    item = MenuItem.query.get_or_404(item_id)
    cart = session.get('cart', {})
    
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'id': item.id,
            'name': item.name,
            'price': str(item.price),
            'quantity': 1
        }
    
    session['cart'] = cart
    return jsonify({'cart_count': sum(item['quantity'] for item in cart.values())})

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

# Admin routes
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_products': MenuItem.query.count(),
        'total_orders': CustomerOrder.query.count(),
        'pending_orders': CustomerOrder.query.filter_by(status='pending').count(),
        'recent_orders': CustomerOrder.query.order_by(CustomerOrder.created_at.desc()).limit(5).all()
    }
    return render_template('admin/dashboard.html', stats=stats)

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
    return render_template('admin/manage_items.html', form=form, items=items)

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
