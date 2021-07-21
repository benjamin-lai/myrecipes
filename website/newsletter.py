from flask import Blueprint, render_template, flash, request, jsonify, current_app as app
from flask_login import current_user
from flask_cors import CORS
from flask_mail import Mail, Message
import json

from . import db
from .models import Users, Profiles, Newsfeeds, Newsletters


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


def welcome_email(user, newsletter):
    topic = "Newsletters"
    body = "Thank you for subscribing to our newsletter service. "
    send_email(user.email, topic, body)

def send_email(email, topic, body):
    mail = Mail(app)
    msg = Message(topic,
        sender='w18b.sheeesh@gmail.com',
        recipients=[email])
    msg.body = body
    msg.html = render_template("home.html", user=current_user)
            
    mail.send(msg)
