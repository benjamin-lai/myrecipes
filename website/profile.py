# Profile Page, I haven't done anything that cool yet.
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users
from .validate_email import validate_email

profile = Blueprint('profile', __name__)
CORS(profile)

# Logged in User's personal profile
@profile.route('/my', methods=['GET', 'POST'])
@login_required
def Profile():
    # static default image hardcoded
    image_file = url_for('static', filename='default_user.jpg')
    backdrop_image = url_for('static', filename='default_backdrop.png')
    return render_template("profile.html", user=current_user, image_file=image_file, backdrop_image=backdrop_image)

@profile.route('/my/edit', methods=['GET', 'POST'])
def update_profile():

    if request.method == 'GET':
        flash('GET triggered', category='error')

    elif request.method == 'POST':
        flash('POST triggered', category='success')

        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_bio = request.form.get('user_bio')
        
        # add login validation here may need to do another validation for username
        user = Users.query.filter_by(email=email).first()       
        if user:
            flash('Email already exists.', category='error')
        elif validate_email(email) is False:
            flash('Email provided is not valid.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 1:        # Remember to change limit
            flash('Password must be at least 7 characters.', category='error')
        else:
            current_user.email = email        
            current_user.first_name = first_name
            current_user.password = password1     
            current_user.bio = user_bio
            db.session.commit()
            Profile()
            return redirect(url_for('profile.Profile'))

    return render_template("edit_profile.html", user=current_user)
# todo:
# 1) Barebones (complete)
# 2) edit profile
# 3) upload and store images
# 4) View other users profile
# 5) recipes function

# profile check
# 1) Display Name (Do we want to differentiate between username/displayname and first name?)
# 2) User Bio
# 3) profile picture
# 4) Edit profile
# 5) subscriber list and count
# 6) Subscribe button
# 7) Recipes
# 8) Banner/background image
# 9) any additional info

# Quality improvements
# 1) profile and update profile may be able to be combined but I want two separate routes.