# Authentication
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import CORS

from .models import Users, Profiles
from .validate_email import validate_email
from . import db


auth = Blueprint('auth', __name__)
CORS(auth)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if login_fn(email, password):
            return redirect(url_for('views.home'))
    
    return render_template("login.html", user=current_user)

def login_fn(email, password):
    user = Users.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return True
    flash('Invalid Email or Password. Please try again', category='error')
    return False



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if sign_up_fn(email, first_name, last_name, password1, password2):
            return redirect(url_for('views.home'))  

    return render_template("sign_up.html", user=current_user)

def sign_up_fn(email, first_name, last_name, password1, password2):

    # Checks if email already exists
    # Similar to    select email from users where email = %s     
    if Users.query.filter_by(email=email).first()  :
        flash('Email already exists.', category='error')
    elif validate_email(email) is False:
        flash('Email provided is not valid.', category='error')
    elif len(first_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif len(last_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 1:        # Remember to change limit
        flash('Password must be at least 7 characters.', category='error')
    else:
        # Register new user
        new_user = Users(email=email, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)        # Adds to our database
        db.session.commit()             # Commits changes

        bio='Not much is known about this user... Encourage them to setup their user bio!'
        # static default image hardcoded
        image_file = url_for('static', filename='default_user.jpg')      

        # Create default profile for new user
        new_profile = Profiles(first_name="", last_name="", display_name=first_name + ' ' +  last_name, profile_pic=image_file, bio=bio, owns=new_user.id)

        db.session.add(new_profile)
        db.session.commit()             # Commits changes

        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return True
    return False