# Backend for the support page which caters for upload images/files support.

from flask import Blueprint, render_template, flash, request, current_app as app
from flask_login import current_user
from flask_cors import CORS
from flask_mail import Mail, Message
import boto3
from werkzeug.utils import secure_filename

s3 = boto3.client('s3',
    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
    aws_secret_access_key= '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'
     )
BUCKET_NAME='comp3900-w18b-sheeesh'


support = Blueprint('support', __name__)
CORS(support)

@support.route('/support', methods=['GET', 'POST'])
def supports():
    if request.method == 'POST':
    # Getting list of integers, that correspond to content they want in their newsletters
        email = request.form.get('email')
        topic = request.form.get('topic_select')
        body = request.form['email-body']
        uploaded_files = request.files.getlist('files')
        
        if email is None:
            flash('Invalid Email address', category='error')

        if topic is None:
            flash('Please select a topic', category='error')

        elif body is None:
            flash('Please enter some description', category='error')

        else:
            # Given the uploaded_files save it into boto3
            for file in uploaded_files:
                if file:
                    filename = secure_filename(file.filename)
                    file.save(filename)
                    s3.upload_file(
                        Bucket = 'comp3900-w18b-sheeesh',
                        Filename=filename,
                        Key = filename
                    )

            # Send information over to our email.
            flash('Successfully sent email!', category='success')
            send_email(email, topic, body, uploaded_files)

    return render_template("support.html", user=current_user)

# Function that sends the query email over to our group email.
def send_email(email, topic, body, files):
    mail = Mail(app)
    msg = Message(topic,
        sender=email,
        recipients=['w18b.sheeesh@gmail.com'])
    msg.body = f"Email from {email}\n\n" + body
    # Go through the attached files again and attach it to our email.
    for f in files:
        if f:
            # Forced to use local images rather than boto3. Since msg.attach takes a 
            #   file rather than a link to our cloud.
            with open(f.filename, 'rb') as images:
                msg.attach(f.filename, f.content_type, images.read())
            
    mail.send(msg)
