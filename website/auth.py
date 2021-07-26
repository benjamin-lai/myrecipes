# Authentication
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import CORS
from flask_mail import Mail, Message
from random import randint

from .models import Subscribed, Subscriber, Users, Profiles, Codes
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
def logout():
    if current_user.is_authenticated:   
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template("restricted_access.html")



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
    elif len(password1) < 7:        # Remember to change limit
        flash('Password must be at least 7 characters.', category='error')
    else:
        # Register new user
        new_user = Users(email=email, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)        # Adds to our database
        db.session.commit()             # Commits changes

        bio="Not much is known about this user... Encourage them to setup their user bio!"
        # static default image hardcoded
        image_file = url_for('static', filename='default_user.jpg')      

        # Create default profile for new user
        new_profile = Profiles(first_name=first_name, last_name=last_name, display_name=first_name + ' ' + 
            last_name, profile_pic=image_file, bio=bio, custom_url=None, owns=new_user.id)

        db.session.add(new_profile)
        db.session.commit()             # Commits changes

        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return True
    return False

@auth.route('/recover', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Checks if provided email exists
        user = Users.query.filter_by(email=email).first()
        if user is None:
            flash('Email does not exist! Please enter a correct email', category='error')
    
        else:
            generate_recovery_code(user)
            flash('Email contain your reset code has been sent to your email!', category='success')
            return redirect(url_for('auth.change_password'))

    return render_template("recover.html")
        

@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        code = request.form.get('reset_code')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if code.isnumeric() is False or len(str(code)) != 6:
            flash('Code is invalid', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:        # Remember to change limit
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Find a generate code table exists for the provided code 
            user_code = Codes.query.filter_by(reset_code=code).first()
            if user_code is not None:
                user = Users.query.filter_by(id=user_code.own).first()
                # Dont need to check if user exists since it should since code is valid.
                
                flash('Successfully changed password!', category='success')
                db.session.delete(user_code)
                user.password = generate_password_hash(password1)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash('Invalid Code, please try again', category='error')
    return render_template("change_pwd.html")
                
        
def generate_recovery_code(user):
     # Generate a recovery code and add it to the table
    reset_code = randint(100000, 999999)

    # Check to see if code table exists for existing email already
    code = Codes.query.filter_by(own=user.id).first()
    if code is not None:
        code.reset_code = reset_code
    else:
        new_code = Codes(own=user.id, reset_code=reset_code)
        db.session.add(new_code)
    db.session.commit()

    # Send the code to user via email.
    send_recovery_code(user.email, reset_code)
    

def send_recovery_code(email, reset_code):
    mail = Mail(app)
    msg = Message(str(reset_code) + ' is your MyRecipe account recovery code',
        sender='w18b.sheeesh@gmail.com',
        recipients=[email])
    msg.body = f'We received a request to reset your MyRecipe password.\nEnter the following password reset code {reset_code}.'
    mail.send(msg)



        
        

