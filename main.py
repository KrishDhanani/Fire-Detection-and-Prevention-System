from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Base(DeclarativeBase):
    pass

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=5)])
    password1 = PasswordField('Re-Enter Password', validators=[DataRequired(), Length(min=5), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensorData.db'
db.init_app(app)

app.config['SECRET_KEY'] = "krish@dhanani"
bootstrap = Bootstrap5(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('FirstPage.html')

@app.route('/Signin')
def signin():
    form = SignInForm()
    return render_template('Signin.html', form=form)

@app.route('/Signup')
def signup():
    form = SignUpForm()
    return render_template('Signup.html', form=form)

@app.route('/buy')
def buy():
    return render_template('Buying.html')

if __name__ == '__main__':
    app.run(debug=True, port=1001)