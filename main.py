import smtplib
from datetime import datetime
import time
import flask
import pytz
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignInForm, SignUpForm, OrderForm
import requests

channel_id = 2527010
THINGSPEAK_API_KEY = "60X95M3U43W68XUI"
parameter = {
    'api_key': THINGSPEAK_API_KEY,
}

My_EMAIL = "krishdhanani7433@gmail.com"
PASSWORD = "qailealdeqpdtulo"


def convert_to_ist(zulu_time_str):
    try:
        # Parse the UTC time string
        zulu_time = datetime.strptime(zulu_time_str, '%Y-%m-%dT%H:%M:%SZ')

        # Define timezone objects
        zulu_timezone = pytz.timezone('UTC')
        indian_timezone = pytz.timezone('Asia/Kolkata')

        # Localize the UTC time to the Indian timezone
        indian_time = zulu_time.replace(tzinfo=zulu_timezone).astimezone(indian_timezone)

        # Format the Indian time and return
        return indian_time.strftime('%H:%M:%S')
    except ValueError as e:
        print("Error converting time:", e)
        return None




# Database Config.
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensorData.db'
db.init_app(app)

app.config['SECRET_KEY'] = "krish@dhanani"
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    # sensor_id: Mapped[int] = mapped_column(unique=True, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('FirstPage.html', current_user=current_user)


@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # check whether user is already in your database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user_email_already_exists = result.scalar()

        result1 = db.session.execute(db.select(User).where(User.phone == form.phone.data))
        user_phone_already_exists = result1.scalar()

        if user_email_already_exists:
            flask.flash('Email already registered...', 'success')
            return redirect(url_for('signin'))

        if user_phone_already_exists:
            flask.flash('Phone Number already registered...', 'success')
            return redirect(url_for('signin'))

        if form.password.data != form.password.data:
            flask.flash('Make Focus and write like both Passwords field match', 'danger')
            return redirect(url_for('signup'))

        else:
            hash_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256:60000',
                salt_length=8,
            )

            name = form.email.data.split('@')
            # print(name)
            new_user = User(
                email = form.email.data,
                phone = form.phone.data,
                password = hash_password
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('Signup.html', form=form, current_user=current_user)


@app.route('/Signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        try:
            user_exist = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        except Exception as e:
            flask.flash("We're unable to find Email", 'danger')
            return redirect(url_for('signup'))
        else:
            if user_exist is None:
                flask.flash("Email not found", 'danger')
                return redirect(url_for('signin'))

            elif user_exist.phone != int(form.phone.data):
                flask.flash("You entered the correct email, but the phone number doesn't match", 'danger')
                return redirect(url_for('signin'))

            elif check_password_hash(user_exist.password, form.password.data):
                login_user(user_exist)
                return redirect(url_for('home'))
            else:
                flask.flash('Invalid Password', 'danger')
                return redirect(url_for('signin'))
    return render_template('Signin.html', form=form, current_user=current_user)

@app.route('/Signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/pricing')
def pricing():
    return render_template('Pricing.html', current_user=current_user)


@app.route("/faqs")
def questions():
    return render_template('FAQs.html', current_user=current_user)


@app.route("/about")
def about():
    return render_template('About.html', current_user=current_user)


@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == "POST":
        user_name = request.form['name']
        user_email = request.form['email']
        user_phone = request.form['phone']
        user_description = request.form['message']

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=My_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=My_EMAIL,
                to_addrs=My_EMAIL,
                msg=f"Subject: Contact from {user_name}! \n\n "
                    f"User name: {user_name} \n "
                    f"Email: {user_email} \n "
                    f"Phone number: {user_phone} \n "
                    f"Description: {user_description}")
            connection.sendmail(
                from_addr=My_EMAIL,
                to_addrs=user_email,
                msg=f"Subject: Contact from FlameWatchers! \n\n "
                    f"Thank you for contacting FlameWatchers! "
            )
            flask.flash('Thank you for contacting FlameWatchers.', 'success')
            return redirect(url_for('contactus'))
    return render_template('contactUs.html', current_user=current_user)

@app.route('/feature')
@login_required
def feature():
    return render_template('Feature.html', current_user=current_user)

# @app.route('/feature')
# @login_required
# def FlameDetectd():
#     with smtplib.SMTP('smtp.gmail.com', 587) as connection:
#         connection.starttls()
#         connection.login(user=My_EMAIL, password=PASSWORD)
#         db.session.execute(db.select(User).where(User.email == current_user.email))
#         connection.sendmail(
#             from_addr=My_EMAIL,
#             to_addrs=My_EMAIL,
#         )
#     return render_template('Feature.html', current_user=current_user)


@app.route('/order/<int:order_id>', methods=["GET", "POST"])
def order(order_id):
    form = OrderForm()
    if form.validate_on_submit():
        user_name = form.name.data
        user_email = form.email.data
        user_phone = form.phone.data
        user_lat = form.lat.data
        user_lon = form.lon.data
        user_address = form.address.data
        user_n_item = form.n_item.data
        user_fs = form.fs.data
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=My_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=My_EMAIL,
                to_addrs=My_EMAIL,
                msg=f"Subject: Contact from {user_name}! \n\n "
                    f"User name: {user_name} \n "
                    f"Email: {user_email} \n "
                    f"Phone number: {user_phone} \n "
                    f"Address_latitude: {user_lat} \n "
                    f"Address_longitude: {user_lon} \n "
                    f"Address_address: {user_address} \n "
                    f"Number_of_item: {user_n_item} \n "
                    f"Fire Safety on or off: {user_fs} (1 then on 0 then off) \n "
            )
            connection.sendmail(
                from_addr=My_EMAIL,
                to_addrs=user_email,
                msg=f"Subject: Contact from {user_name}! \n\n "
                    "Thank you for Ordering FlameWatchers Device! \n\n"
                    "Data Given By your side: \n\n"
                    f"User name: {user_name} \n\n "
                    f"Email: {user_email} \n\n "
                    f"Phone number: {user_phone} \n\n "
                    f"Address_latitude: {user_lat} \n\n "
                    f"Address_longitude: {user_lon} \n\n "
                    f"Address_address: {user_address} \n\n "
                    f"Number_of_item: {user_n_item} \n\n "
                    f"Fire Safety on or off: {user_fs} (1 then on and 0 then off) \n\n "
            )
            flask.flash('Thank you for Ordering FlameWatchers Device.', 'success')
            return redirect(url_for('order', order_id=order_id))
    return render_template('Order.html', form=form, order_id=order_id, current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True, port=1001)

