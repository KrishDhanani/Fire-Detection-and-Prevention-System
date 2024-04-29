from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo
from flask_ckeditor import CKEditorField

# SignIn Form
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Sign In')

# Sign Up Form
class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=5)])
    password1 = PasswordField('Re-Enter Password', validators=[DataRequired(), Length(min=5), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

# Order form
class OrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone no.', validators=[DataRequired(), Length(min=10, max=10)])
    lat = StringField('Address latitude', validators=[DataRequired()])
    lon = StringField('Address longitude', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    n_item = IntegerField('No. of item', validators=[DataRequired()])
    fs = StringField("Fire safety (Will the fire safety measures be active during the time when there's a risk of electricity-related shocks?) On or Off? if On then write '1' otherwise '0'.", validators=[DataRequired()])
    submit = SubmitField('Order')