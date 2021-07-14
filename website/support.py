from flask import Blueprint, render_template, flash, request, current_app as app
from flask_login import login_required, current_user
from flask_cors import CORS
from flask_mail import Mail, Message

from . import db
from .models import Users, Profiles, Newsfeeds


support = Blueprint('support', __name__)
CORS(support)

@support.route('/support', methods=['GET', 'POST'])
def supports():
    if request.method == 'POST':
        # Getting list of integers, that correspond to content they want in their newsletters
        topic = request.form.get('topic_select')
        body = request.form['email-body']
        
        if topic is None:
            flash('Please select a topic', category='error')

        elif body is None:
            flash('Please enter some description', category='error')

        else:
            # Send information over to our email.
            flash('Successfully sent email!', category='success')
            send_email(current_user.email, topic, body)

    return render_template("support.html", user=current_user)

def send_email(email, topic, body):
    mail = Mail(app)
    msg = Message(topic,
        sender=email,
        recipients=['w18b.sheeesh@gmail.com'])
    msg.body = body
    mail.send(msg)