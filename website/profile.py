# Profile Page, I haven't done anything that cool yet.
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Profiles, Subscribed_To_Lists, Subscriber_Lists
from .validate_email import validate_email
import boto3
from werkzeug.utils import secure_filename


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
        print('asd')
        image_file = url_for('static', filename='default_user.jpg') 
        backdrop_image = url_for('static', filename='default_backdrop.png')
    else:
        print(profile.profile_pic)
        image_file = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'comp3900-w18b-sheeesh','Key': profile.profile_pic})
        backdrop_image = url_for('static', filename='default_backdrop.png')
    return render_template("profile.html", profile=profile, user=current_user, image_file=image_file, backdrop_image=backdrop_image)


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
            # QOL: If users don't change their email or leave password blank it will keep their current settings
            # Note change display_name to username don't make it confusing
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
            elif custom_url.isdigit():
                flash('Your custom URL cannot be made up of numbers only', category='error')
            else:
                current_user.email = email        
                current_user.username = username
                if len(password1) > 0:
                    current_user.password = password1     
                profile.display_name = username
                if custom_url != "":
                    profile.custom_url = custom_url
                else:
                    profile.custom_url = None
                profile.first_name = first_name
                profile.last_name = last_name
                profile.bio = user_bio
                print("BIO IS " + profile.bio)
                
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

    if request.method == "POST":
    
        sub_state = request.form.get('subscribe')
        if sub_state == "Subscribe":
            flash("Subscribed to this user!", category="sucess")
        elif sub_state == "Subscribed":
            flash("Unsubscribed to this user!", category="error")

    # code for subscribing, contains is the subject user, id is the target
    '''
    if subbing:
        new_subbed = Subscriber_Lists(subscriber_id = current_user.id, contains = public_user.id) # profile's sublist
        new_subber = Subscribed_To_Lists(subscribed_id = public_user.id, contains = current_user.id) # user's subscriptions
        db.session.add(new_subbed)
        db.session.add(new_subber)
    # code for unsubscribing
    elif unsubbing:
        del_subbed = Subscriber_Lists.query.filter_by(subscriber_id = current_user.id, contains = public_user.id)
        del_subber = Subscribed_To_Lists.query.filter_by(subscribed_id = public_user.id, contains = current_user.id)
        db.session.delete(del_subbed)
        db.session.delete(del_subber)

    db.session.commit()
    '''
    if public_user:
        if public_profile.profile_pic == "/static/default_user.jpg":
            image_file = url_for('static', filename='default_user.jpg') 
        else:
            image_file = s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'comp3900-w18b-sheeesh','Key': public_profile.profile_pic})

        return render_template("public_profile.html", profile=public_profile, user=public_user, image_file=image_file, backdrop_image=backdrop_image)
    else:
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))

#potential bug if user sets custom url to a number then when a new user signs up at that number theres a url conflict.

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

        return render_template("public_profile.html", profile=public_profile, user=public_user, image_file=image_file, backdrop_image=backdrop_image)
    else:
        flash("No user exists with this id.", category="error")
        return redirect(url_for('views.home'))


# todo:

# Make profile custom url. -> add url attribute to profiles database so we can make sure it is unique
# later add tooltips for forms.
# Sub plan -> Subscribe button, becomes deactivated when subscribed and text changes.
# either have a hover that says unsubscribe or have an alert on click.

# 1) recipes function
#

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