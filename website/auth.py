# Authentication
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app, session, abort, request
from werkzeug.datastructures import Authorization
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import CORS
from flask_mail import Mail, Message
from random import randint

from .models import Subscribed, Subscriber, Users, Profiles, Codes
from .validate_email import validate_email
from . import db
import os
import pathlib

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
import random
import string


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
    
    
    
    
# Google Sign in API stuff below
    
GOOGLE_CLIENT_ID = "1093754390854-jrpchfpcg1frsjd0m3866dp5gites03b.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            


flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

@auth.route('/google_login', methods=['GET', 'POST'])
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"]  = state
    return redirect(authorization_url)

@auth.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    
    if not session["state"] == request.args["state"]:
        abort(500)
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )



    first_name = id_info.get("given_name")
    last_name = id_info.get("family_name")
    email = id_info.get("email")
    
    # If the user logs in through google sign in, then checks if their gmail already exists
    # instead of an error, it logs into their account this time as they already authenticated
    # through google and they dont need to use login form to log in
    if Users.query.filter_by(email=email).first()  :
        user = Users.query.filter_by(email=email).first()
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home')) 
    
    # if one of the fields needed is not found from gmail account, then prompts them to add it
    # before they can make an account
    if first_name is None or last_name is None or email is None:
        flash('Gmail account must contain first name, last name and email to create an account.', category='error')
        return render_template("login.html")
    
    # create a random temporary password for the user.
    characters = string.ascii_letters + string.digits + string.punctuation
    rand_pass = ''.join(random.choice(characters) for i in range(12))
    
    # creates the account in the database and sends an email to the user's email with their temporary password which can be used to log in through the login form
    # but they can just log in through google sign in as it would be much easier, but just a backup way to log in
    if sign_up_google(email, first_name, last_name, rand_pass):
        topic = "Temporary Password for myRecipes"
        body = "Your temporary password is: " + rand_pass + "\n" + "You can use your gmail address and the temporary password to login through our login system or login through the Google Sign-In using your gmail account.\n" "Also, you can reset the password by using the \"Forgot Password?\" link on the sign on page."
        send_email(email, topic, body)
        return redirect(url_for('views.home')) 
    
    

    return redirect(url_for('views.home'))


def sign_up_google(email, first_name, last_name, password):

     
    if len(first_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif len(last_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    else:
        # Register new user
        new_user = Users(email=email, password=generate_password_hash(password, method='sha256'))
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




def send_email(emails, topic, body):
    mail = Mail(app)
    msg = Message(topic,
        sender='w18b.sheeesh@gmail.com',
        recipients=[emails])
    msg.body = body
            
    mail.send(msg)



        
        

