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
        return render_template("newsletters.html", user=current_user)
    return render_template("restricted_access.html")
    
@newsletter.route('/subscribe-to-newsletters', methods=['POST'])
def subscribe_newsletter():
    if request.method == 'POST':
        # Getting list of integers, that correspond to content they want in their newsletters
        checkbox = json.loads(request.data)
        checkbox_value = checkbox['checkboxes']

        # Check if newsletter already exists for user.
        newsletter = Newsletters.query.filter_by(own=current_user.id).first()
        trending = 0            # set as false initially.
        subscribed_to = 0

        # Switches to on if conditions are met.
        for selected in checkbox_value:
            if selected == '1':             
                trending = 1
            if selected == '2':
                subscribed_to = 1
            
        # Update current newsletter
        if newsletter:
            newsletter.trending = trending
            newsletter.subscribed_to = subscribed_to
        
        else:   # Newsletter does not exist
            newsletter = Newsletters(trending=trending, 
                subscribed_to=subscribed_to, own=current_user.id)
            db.session.add(newsletter)

        flash("Your Newsletter Feed is now updated!", category="success")
        db.session.commit()

        # Send a welcoming email
        welcome_email(current_user, newsletter)
        
    return jsonify({})


@newsletter.route('/unsubscribe-to-newsletters', methods=['POST'])
def unsubscribe_newsletter():
    # Check if the newsletter table exists.
    user_newsletter = Newsletters.query.filter_by(own=current_user.id).first()
    if user_newsletter is not None:
        flash("You have successfully unsubscribed to newsletters", category="success")
        db.session.delete(user_newsletter)
        db.session.commit()
    else:
        flash("You are already unsubscribed to this service", category="error")

    return jsonify({})

# Confirmation email to tell users that they are subscribed to our newsletter service
def welcome_email(user, newsletter):
    topic = "Newsletters"
    body = "Thank you for subscribing to our newsletter service. "
    send_email(user.email, topic, body)

# Method to send a email to provide emails
def send_email(emails, topic, body):
    mail = Mail(app)
    msg = Message(topic,
        sender='w18b.sheeesh@gmail.com',
        recipients=[emails])
    msg.body = body
    msg.html = render_template("home.html")
            
    mail.send(msg)

def send_new_recipe_emails(recipe):
    # Given the recipe
    # Get the subscribers that are following this user.
    user = Profiles.query.filter_by(owns=recipe.creates).first()
    
    # Get user's subscriber list
    subscriber_list = Subscriber.query.filter_by(contains=user.profile_id).all()

    # Get subscribers profile's emails
    emailing_list = get_profile_emails(subscriber_list) 

    if len(emailing_list) != 0:
        topic = f"{user.display_name} has posted a new recipe called {recipe.name}."
        body = f"New recipe can be found at: /{recipe.name}.{recipe.id}"

        # send_email(emailing_list, topic, body)

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

# Email the trending recipe for that week to everyone who is subscribed to that feature 
def send_weekly_trending_recipes(trending):
    # Given the trending recipe
    # Send emails to everyone subbed to trending feature
    newsletters = Newsletters.all()

    # Get user email
    emailing_list = get_trending_emails(newsletters)

    if len(emailing_list) != 0:
        topic = "New weekly trending recipes!"
        body = "New recipe"

        send_email(emailing_list, topic, body)


def get_trending_emails(newsletter_list):
    emailing_list = []
    for newsletter in newsletter_list:
        if newsletter.trending == True:
            user = Users.query.filter_by(id=newsletter.own).first()
            emailing_list.append(user.email)
    return emailing_list