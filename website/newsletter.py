from flask import Blueprint, render_template, flash, request, jsonify, current_app as app
from flask_login import current_user
from flask_cors import CORS
from flask_mail import Mail, Message
import json

from . import db
from .models import Subscriber, Users, Profiles, Newsfeeds, Newsletters


newsletter = Blueprint('newsletter', __name__)
CORS(newsletter)


@newsletter.route('/manage_newsletters', methods=['GET', 'POST'])
def manage_newsletter():
    if current_user.is_authenticated:     
        # This is  what the users will be looking at, every other method down 
        #   below are functions that assist in the subscribe/unsubscribe process. 
        return render_template("newsletters.html", user=current_user)
    return render_template("restricted_access.html")                        
    
@newsletter.route('/subscribe-to-newsletters', methods=['POST'])
def subscribe_newsletter():
    if request.method == 'POST':
        # Check if newsletter already exists for user.
        newsletter = Newsletters.query.filter_by(own=current_user.id).first()
            
        # Update current newsletter
        if newsletter:
            newsletter.subscribed_to = 1
            flash("Your Newsletter Feed is now updated!", category="success")
        
        else:   # Newsletter does not exist
            newsletter = Newsletters(subscribed_to=1, own=current_user.id)
            db.session.add(newsletter)
            flash("You have successfully subscribed to this service!", category="success")

        db.session.commit()
    return jsonify({})


@newsletter.route('/unsubscribe-to-newsletters', methods=['POST'])
def unsubscribe_newsletter():
    # Check if the newsletter table exists.
    user_newsletter = Newsletters.query.filter_by(own=current_user.id).first()
    if user_newsletter is not None:
        flash("You have successfully unsubscribed to newsletters", category="success")
        user_newsletter.subscribed_to = 0
        db.session.commit()
    else:
        flash("You are already unsubscribed to this service", category="error")

    return jsonify({})

# Method to send a email to provide emails
def send_email(emails, topic, body):
    mail = Mail(app)
    msg = Message(topic,
        sender='w18b.sheeesh@gmail.com',
        body = body)

    # Recipients requires a list
    # However, it does not take a list inside a list i.e. [ [recipients] ]
    if type(emails) is type([]):        # Avoids the issue above.
        msg.recipients = emails
    else:                               # Caters for when there is only one user.
        msg.recipients = [emails] 
            
    mail.send(msg)

def send_new_recipe_emails(recipe):
    # Given the recipe
    # Get the subscribers that are following this user.
    user = Profiles.query.filter_by(owns=recipe.creates).first()
    
    # Get user's subscriber list
    subscriber_list = Subscriber.query.filter_by(contains=user.profile_id).all()

    # Get subscribers profile's emails
    emailing_list = get_profile_emails(subscriber_list) 
    print(emailing_list)
    if len(emailing_list) != 0:
        topic = f"{user.display_name} has posted a new recipe called {recipe.name}."
        body = f"New recipe can be found at: http://127.0.0.1:5000/{recipe.name}.{recipe.id}"

        send_email(emailing_list, topic, body)

# Get the list of emails who are subscribed to the user and accepts newsletters
def get_profile_emails(sub_list):
    emailing_list = []
    for sub in sub_list:
        user = Users.query.filter_by(id=sub.subscriber_id).first()

        # Check if user is subscribed to newsletter and is accepts newsletter
        #   for when their subscribed user posts
        newsletter = Newsletters.query.filter_by(own=user.id).first()
        if newsletter:
            if newsletter.subscribed_to == True:
                emailing_list.append(user.email)
    return emailing_list