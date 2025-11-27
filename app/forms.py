from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class MenuItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', choices=[
        ('Coffee', 'Coffee'),
        ('Tea', 'Tea'),
        ('Dessert', 'Dessert')
    ], validators=[DataRequired()])
    image = FileField('Item Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only! (jpg, jpeg, png)')
    ])
    is_available = BooleanField('Available', default=True)

class OrderForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    notes = TextAreaField('Special Instructions', validators=[Optional(), Length(max=500)])
