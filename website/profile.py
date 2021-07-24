# Profile Page, I haven't done anything that cool yet.
import os
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Recipes, Users, Profiles, Subscribed, Subscriber, profile_subs, profile_subbed, Cookbooks_lists
from .validate_email import validate_email
import boto3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import json

profile = Blueprint('profile', __name__)
CORS(profile)

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='comp3900-w18b-sheeesh'

# Current user's personal profile (Logged in)
@profile.route('/my', methods=['GET', 'POST'])
@login_required
def Profile():
    # backdrop hardcoded, add to database later for additional feature
    profile = Profiles.query.filter_by(profile_id=current_user.id).first() 
    # this removes any temp_pics incase they cancelled or went back a page after uploading the pic
    profile.temp_pic = None
    db.session.commit()
    if profile.profile_pic == "/static/default_user.jpg":
        image_file = url_for('static', filename='default_user.jpg') 
        backdrop_image = url_for('static', filename='default_backdrop.png')
    else:
        image_file = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'comp3900-w18b-sheeesh','Key': profile.profile_pic})
        backdrop_image = url_for('static', filename='default_backdrop.png')

        
    return view_profile1(profile.custom_url)


@profile.route('/my/edit', methods=['GET', 'POST'])
def update_profile():
    profile = Profiles.query.filter_by(profile_id=current_user.id).first() 
    
    if request.method == 'POST':
        if request.form['button'] == "Upload":
             img = request.files['file']
             if img:  
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = 'comp3900-w18b-sheeesh',
                    Filename=filename,
                    Key = filename
                )
                os.remove(filename)
                profile.temp_pic = filename
                db.session.commit()
    
    
    if request.method == 'POST':
        if request.form['button'] == "Submit":
            username = request.form.get('username')
            email = request.form.get('email')
            custom_url = request.form.get('custom_url')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            user_bio = request.form.get('user_bio')
            
            
            # add login validation here may need to do another validation for username
            # QOL: Change all flashes to tooltips later
            email_check = Users.query.filter_by(email=email).first()    
            url_check = Profiles.query.filter_by(custom_url=custom_url).first()  
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
            elif url_check and url_check.profile_id!=current_user.id and len(url_check.custom_url)>0:
                flash('The specified profile URL is already in use', category='error')
            elif custom_url.isdigit() and int(custom_url) != profile.profile_id:
                flash('Your custom URL cannot be made up of numbers only', category='error')
            elif len(password1) > 0 and check_password_hash(current_user.password, password1):
                flash('The new password you entered is the same as your previous password!', category='error')
            else:
                current_user.email = email        
                current_user.username = username
                if len(password1) > 0 :
                    current_user.password = generate_password_hash(password1, method='sha256')  
 
                profile.display_name = username
                if custom_url != "":
                    profile.custom_url = custom_url
                else:
                    profile.custom_url = profile.profile_id
                profile.first_name = first_name
                profile.last_name = last_name
                profile.bio = user_bio
                
                if profile.temp_pic is not None:
                    profile.profile_pic = profile.temp_pic
                    profile.temp_pic = None
                
                
                db.session.commit()
                Profile()
                flash("Profile Updated!", category='success') #also flashes when no change happens
                return redirect(url_for('profile.Profile'))

    return render_template("edit_profile.html", user=current_user, profile=profile)

@profile.route('/<custom_url>', methods=["GET", "POST"]) # public view of profile based off a url set by the user
def view_profile1(custom_url):
    # maybe try no digit
    try:
        public_profile = Profiles.query.filter_by(custom_url=custom_url).first()
        public_user = Users.query.filter_by(id=public_profile.profile_id).first()
    except:
        flash("No user exists with this username or id.", category="error")
        return redirect(url_for('views.home'))
    # backdrop hardcoded -> when backdrop image is added to edit profile we can remove this
    # as this generates a public profile based off w/e is in the database
    backdrop_image = url_for('static', filename='default_backdrop.png')
  
    if public_user:
        if public_profile.profile_pic == "/static/default_user.jpg":
            image_file = url_for('static', filename='default_user.jpg') 
        else:
            image_file = s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'comp3900-w18b-sheeesh','Key': public_profile.profile_pic})

        # display personal recipes
        query = Recipes.query.filter_by(creates=public_user.id)
        if (current_user.is_authenticated):
            sub_status = Subscriber.query.filter_by(subscriber_id = current_user.id, contains = public_profile.profile_id).first()
            if not sub_status:
                sub_status = "unsubbed"
            else:
                sub_status = "subbed"
        else:
            sub_status = "unsubbed"
        
        subs = Subscriber.query.filter_by(contains = public_profile.profile_id).count()
        return render_template("public_profile.html", profile=public_profile, user=public_user, image_file=image_file, 
            backdrop_image=backdrop_image, query=query, sub_status = sub_status, subs=subs)
    else:
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))

# background process that subscribes users on button press without refreshing the page
@profile.route('/subscribe', methods=["GET", "POST"])
def profile_sub():
    message = ""
    if request.method == "POST":
        sub_status = request.form['status']
        user_id = request.form['user']
        profile_id = request.form['profile']
        # sub_status = "subscribe" or "subscribed" with the quotations included. Later add an alert for unsubscribing and make sure only s
        # logged in users can subscribe. Can't subscribe to yourself (maybe add this).
    if str(sub_status) == '"Subscribed"':
        new_subbed = Subscribed(subscribed_id = profile_id, contains = user_id) # user's subscribed to list
        new_subber = Subscriber(subscriber_id = user_id, contains = profile_id) # profile's sublist
        db.session.add(new_subbed)
        db.session.add(new_subber)
        
        message = "user " + str(user_id) + " has subscribed to " + str(profile_id)
    # code for unsubscribing
    elif str(sub_status) == '"Subscribe"':
        del_subber= Subscriber.query.filter_by(subscriber_id = user_id, contains = profile_id).first()
        del_subbed = Subscribed.query.filter_by(subscribed_id = profile_id, contains = user_id).first()
        db.session.delete(del_subbed)
        db.session.delete(del_subber)
        message = "user " + str(user_id) + " has unsubscribed to " + str(profile_id)

    db.session.commit()
    return (message)

# subscribers list
@profile.route('/<custom_url>/subscribers', methods=["GET", "POST"])
def subscriber_list(custom_url):
    try:    
        public_profile = Profiles.query.filter_by(custom_url=custom_url).first()
        public_user = Users.query.filter_by(id=public_profile.profile_id).first()
    except:
        flash("No user exists with this username or id.", category="error")
        return redirect(url_for('views.home'))

    subbers = profile_subs.query.filter_by(contains = public_profile.profile_id).all()
    sub_count = profile_subs.query.filter_by(contains = public_profile.profile_id).count()
    for sub in subbers:
        sub.sub_count = profile_subs.query.filter_by(contains = sub.profile_id).count()
        sub.recipe_count = Recipes.query.filter_by(creates=sub.profile_id).count()

    # add code for profiles with no subs
    type = "subscribers"
    return render_template("subscriber_list.html", profile=public_profile, user=public_user, query=subbers, sub_count=sub_count, type=type)

# subscribed-to list
@profile.route('/<custom_url>/subscriptions', methods=["GET", "POST"])
def subscribed_list(custom_url):
    try:    
        public_profile = Profiles.query.filter_by(custom_url=custom_url).first()
        public_user = Users.query.filter_by(id=public_profile.profile_id).first()
    except:
        flash("No user exists with this username or id.", category="error")
        return redirect(url_for('views.home'))
    
    subbed = profile_subbed.query.filter_by(contains = public_profile.profile_id).all()
    sub_count = profile_subbed.query.filter_by(contains = public_profile.profile_id).count()
    for sub in subbed:
        sub.sub_count = profile_subs.query.filter_by(contains = sub.profile_id).count()
        sub.recipe_count = Recipes.query.filter_by(creates=sub.profile_id).count()

    # add code for profiles with no subs
    type = "subscriptions"
    return render_template("subscriber_list.html", profile=public_profile, user=public_user, query=subbed, sub_count=sub_count)

@profile.route('/<int:id>', methods=["GET", "POST"]) # public view of profile based off id 
def view_profile(id):
    try:
        public_user = Users.query.filter_by(id=id).first()
        public_profile = Profiles.query.filter_by(profile_id=id).first()
    except:
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))
    # backdrop hardcoded -> when backdrop image is added to edit profile we can remove this
    # as this generates a public profile based off w/e is in the database
    backdrop_image = url_for('static', filename='default_backdrop.png')
    
    if public_user and public_profile:
        if public_profile.profile_pic == "/static/default_user.jpg":
            image_file = url_for('static', filename='default_user.jpg') 
        else:
            image_file = s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'comp3900-w18b-sheeesh','Key': public_profile.profile_pic})
        # display personal recipes
        query = Recipes.query.filter_by(creates=public_user.id)
        
        return view_profile1(public_profile.custom_url)
    else:
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))


#cookbook in profile
@profile.route('/cookbook', methods=['GET','POST']) # public view of profile based off name and id
def cook_book():
    #implementing create

    #delete

    #name changing

    #add recipes

    #delete recipes


    cookbook_all = Cookbooks_lists.query.all()
    return render_template("cookbook.html",user = current_user)



# todo:

# Edit display recipes


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
# 1) Fix up code for view public profile, try/except the whole thing
# 2) add a button to personal profile page that allows them to check how their profile looks in public (similar to facebook)


