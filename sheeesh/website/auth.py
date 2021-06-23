from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

from .validate_email import validate_email
from .models import create_account

auth = Blueprint('auth', __name__)
CORS(auth)

@auth.route('/recipe', methods=['GET', 'POST'])
def recipe():
    data = request.form
    print(data)
    return recipe()

def recipe():
    return render_template("recipe.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return login_fn()

def login_fn():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>You have signed out</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')   # Confimation

        if sign_up_fn(email, first_name, password1, password2):
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")

def sign_up_fn(email, first_name, password1, password2):
    #print(f"{email}, {first_name}, {password1}, {password2}")

    if validate_email(email) is False:
        flash("This email is invalid.", category='error')
    elif len(first_name) < 1:
        flash("Invalid First Name", category='error')
    elif password1 != password2:
        flash("Passwords do not match", category='error')
    elif len(password1) < 1:
        flash("Password much be at least 7 characters long", category='error')
    else:
        create_account(email, first_name, password1)
        flash("Account Created!", category='success')
        return True
    return False
