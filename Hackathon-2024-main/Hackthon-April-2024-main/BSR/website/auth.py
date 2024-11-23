from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
# from . import db
from flask_mongoengine import MongoEngine
from mongoengine import Document, ListField, DictField, DateTimeField, StringField
import datetime

db = MongoEngine()


auth = Blueprint('auth', __name__)

@auth.route('/home')
def home():
    return render_template("home.html")

class Login(Document):
    user_id = StringField(required=True)
    password = StringField(required=True)
    notes = DictField()
    date = DateTimeField(default=datetime.datetime.now)

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        # Using the 'Login' class to query the user
        user = Login.objects(user_id=user_id).first()
        if user:
            # Logged in Successfully
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.portal'))
            # Incorrect Password
            else:
                flash('Incorrect password, try again.', category='error')
        # Incorrect User ID
        else:
            flash('User ID does not exist.', category='error')
            
    # Inside your login route, after validating the user
    if user and check_password_hash(user.password, password):
    # Save the successful login attempt
        login_attempt = Login(
        user_id=user_id,
        password='dummy_password',  # Replace with a hashed dummy password or remove if not needed
        notes={'note': 'Successful login attempt'},
        date=datetime.datetime.now()
    )
        login_attempt.save()
    else:
     # Save the failed login attempt
        login_attempt = Login(
        user_id=user_id if user else 'anonymous',
        password='dummy_password',  # Replace with a hashed dummy password or remove if not needed
        notes={'note': 'Failed login attempt'},
        date=datetime.datetime.now()
    )
    login_attempt.save()
    return render_template("login.html", user=current_user)

# Logged Out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


class Profile(db.Document):
    user_type = db.StringField(required=True)
    user_id = db.StringField(required=True)
    name = db.StringField(required=True)
    date = db.DateField(required=True)
    email = db.StringField(required=True)
    mobile_number = db.StringField(required=True)
    password = db.StringField(required=True)
    gender = db.StringField(required=True)
    address = db.StringField(required=True)


# Register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type= request.form.get('user_type')
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        date= request.form.get('date')
        email = request.form.get('email')
        mobile_number= request.form.get('mobile_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender= request.form.get('gender')
        address= request.form.get('address')

        user = Profile.find_one({"user_id": user_id})
        if user:
            flash('User ID already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='sha256')
            new_user = {  
                "user_id": user_id,
                "password": hashed_password,  
                "user_type": user_type,
                "name": name,
                "date": date,
                "email": email,
                "mobile_number": mobile_number,
                "gender": gender,
                "address": address,
            }
            user_id = Profile.insert_one(new_user).inserted_id
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.portal'))

    return render_template("register.html", user=current_user)