from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from forms import SignInForm, SignUpForm

class Base(DeclarativeBase):
    pass


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

@app.route('/pricing')
def pricing():
    return render_template('Buying.html')

@app.route("/faqs")
def questions():
    return render_template('FAQs.html')

@app.route("/about")
def about():
    return render_template('About.html')

if __name__ == '__main__':
    app.run(debug=True, port=1001)