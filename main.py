import os
from datetime import datetime
import time

import pytz
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from forms import SignInForm, SignUpForm, OrderForm
import requests


THINGSPEAK_API_KEY = "60X95M3U43W68XUI"
parameter = {
    'api_key': THINGSPEAK_API_KEY,
}
response = requests.get(url='https://api.thingspeak.com/channels/2527010/feeds.json', params=parameter)
response.raise_for_status()
data = response.json()
print(data)

def convert_to_ist(zulu_time_str):
    try:
        zulu_time = datetime.strptime(zulu_time_str, '%Y-%m-%dT%H:%M:%SZ')
        zulu_timezone = pytz.timezone('UTC')
        indian_timezone = pytz.timezone('Asia/Kolkata')
        indian_time = zulu_timezone.localize(zulu_time).astimezone(indian_timezone)
        return indian_time.strftime('%H:%M:%S')
    except ValueError as e:
        print("Error converting time:", e)
        return None


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
    return render_template('Pricing.html')

@app.route("/faqs")
def questions():
    return render_template('FAQs.html')

@app.route("/about")
def about():
    return render_template('About.html')

@app.route('/contactus')
def contactus():
    return render_template('contactUs.html')

@app.route('/feature')
def feature():
    return render_template('Feature.html')

@app.route('/order/<int:order_id>')
def order(order_id):
    form = OrderForm()
    return render_template('Order.html', form=form, order_id=order_id)

if __name__ == '__main__':
    app.run(debug=True, port=1001)

while True:
    response = requests.get(url='https://api.thingspeak.com/channels/2527010/feeds.json', params=parameter)
    response.raise_for_status()
    data = response.json()['feeds']
    zulu_time = data[len(data) - 1]['created_at'][11:].replace('T', ' ').replace('Z', '')

    print(data)
    if int(data[len(data) - 1]['field1']) == 1:
        print("Flame Not detected \nIndian time:", datetime.now().time())
    if int(data[len(data)-1]['field1']) == 0:
        flame_detected_time = convert_to_ist(zulu_time)
        if flame_detected_time:
            print("Flame Sensor ID:", data['field2'], "\nFlame Detected Time (IST):", flame_detected_time)
    time.sleep(15)