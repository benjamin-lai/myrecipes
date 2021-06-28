# Profile Page, I haven't done anything that cool yet.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db

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
        # add login validation here
        return redirect(url_for("profile.Profile"))

    return render_template("edit_profile.html", user=current_user)
# todo:
# 1) Barebones
# 2) edit profile
# 3) upload and store images
# 4) Access other users profile
# 5) recipes function

#basic profile check
# 1) Display Name
# 2) User Bio
# 3) profile picture
# 4) Edit profile
# 5) subscriber list and count
# 6) Subscribe button
# 7) Recipes
# 8) Any additional info if we want

