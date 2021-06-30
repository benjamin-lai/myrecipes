# Profile Page, I haven't done anything that cool yet.
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Profiles
from .validate_email import validate_email

profile = Blueprint('profile', __name__)
CORS(profile)

# Current user's personal profile (Logged in)
@profile.route('/my', methods=['GET', 'POST'])
@login_required
def Profile():

    # backdrop hardcoded, add to database later for additional feature
    backdrop_image = url_for('static', filename='default_backdrop.png')
    profile = Profiles.query.filter_by(profile_id=current_user.id).first() 
    return render_template("profile.html", profile=profile, user=current_user, backdrop_image=backdrop_image)

@profile.route('/my/edit', methods=['GET', 'POST'])
def update_profile():
    profile = Profiles.query.filter_by(profile_id=current_user.id).first() 
    print ("TEST TEST " + profile.display_name)
    if request.method == 'POST':

        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_bio = request.form.get('user_bio')
        
        # add login validation here may need to do another validation for username
        # QOL: If users don't change their email or leave password blank it will keep their current settings
        # Note change display_name to username don't make it confusing
        email_check = Users.query.filter_by(email=email).first()      
        if email_check and email_check!=current_user:
            flash('Email already exists.', category='error')
        elif validate_email(email) is False:
            flash('Email provided is not valid.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif 0 < len(password1) < 1:        # Remember to change limit
            flash('Password must be at least 7 characters.', category='error')
        else:
            current_user.email = email        
            current_user.username = username
            if len(password1) > 0:
                current_user.password = password1     
            profile.display_name = username
            profile.first_name = first_name
            profile.last_name = last_name
            profile.bio = user_bio
            db.session.commit()
            Profile()
            flash("Profile Updated!", category='success') #also flashes when no change happens
            return redirect(url_for('profile.Profile'))

    return render_template("edit_profile.html", user=current_user, profile=profile)

@profile.route('/<id>') # public view of profile #id (same as profile but without edit option)
def view_profile(id):
# Possible change is to use username instead of id for the route but we would have to add an underscore instead of spaces
# for usernames that include spaces
    if not id.isdigit():
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))

    public_user = Users.query.filter_by(id=id).first()
    public_profile = Profiles.query.filter_by(profile_id=id).first()
    
    # backdrop hardcoded -> when backdrop image is added to edit profile we can remove this
    # as this generates a public profile based off w/e is in the database
    backdrop_image = url_for('static', filename='default_backdrop.png')

    if public_user and public_profile:
        return render_template("public_profile.html", profile=public_profile, user=public_user, backdrop_image=backdrop_image)
    else:
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))




# todo:
# 2) BUG: logged out users appear logged in 
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