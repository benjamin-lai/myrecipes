# Profile Page, I haven't done anything that cool yet.
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Profiles
from .validate_email import validate_email
import boto3
from werkzeug.utils import secure_filename
from .models import Users, Recipes, Ingredient, Contents, Recipestep, Profiles,Method,Meal_Type,newsletter_email
from .validate_email import validate_email

import smtplib
import email# 负责构造文本
from email.mime.text import MIMEText# 负责构造图片
from email.mime.image import MIMEImage# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

newsletter = Blueprint('newsletter', __name__)
CORS(newsletter)

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='comp3900-w18b-sheeesh'

searchInput = ""

#global variables use to save filters
IngredientFilter = []
MethodFilter = []
MealTypeFilter = ""
SortBy = ""

@newsletter.route('/newsletter', methods=['GET','POST'])  
def newsletter_support():
    if request.method == 'POST':
        newsletter_sub = request.form.get('newsletter')
        if newsletter_sub is not None:  #clicked newsletter submit
            email = request.form.get('email_input')
            print(email)
            if validate_email(email) is False:
                flash('Email provided is not valid.', category='error')
            elif newsletter_email.query.filter_by(email = email).first():
                flash('Email already exists.', category='error')
            else:
                #add to db
                new_newsletter = newsletter_email(email = email)
                db.session.add(new_newsletter)
                db.session.commit()
                print("added to db")

                #try to send a welcome message to new user
                send_welcome_email(email)
                flash("Thank you for subscribing")
                return render_template("newsletter.html",user = current_user)
        support_sub = request.form.get('support')
        if support_sub is not None:  #clicked support submit
            support_input = request.form.get('support_input')
            if len(support_input) < 1:
                flash("support input can not be empty", category='error')
            else:
                flash("Thanks for your feedback")
                #send the support to our official email address
                send_support_email(support_input)
                return render_template("newsletter.html",user = current_user)
    return render_template("newsletter.html",user = current_user)

def send_welcome_email(email_address):
    #SMTP server, use 163 mailbox
    mail_host = "smtp.163.com"
    #sender(us) email
    mail_sender = "MyRecipeOfficial@163.com"
    mail_license = "AKZSQAFMQTBPWEOC"
    #Addressee email
    mail_receivers = email_address

    mm = MIMEMultipart('related')

    #4.email heading parts
    subject_content = "MyRecipe [Newsletter]"
    mm["From"] = f"sender_name<{mail_sender}>"
    mm["To"] = f"receiver_name<{mail_receivers}>"
    #theme
    mm["Subject"] = Header(subject_content,'utf-8')

    #5.email text
    body_content = "Welcome to MyRecipe's Newsletter, we will push our new trendings to your email."
    message_text = MIMEText(body_content,"plain","utf-8")
    mm.attach(message_text)


    #6.add a image
    image_data = open('website/static/Images/maxresdefault.jpeg','rb')
    message_image = MIMEImage(image_data.read())
    image_data.close()
    mm.attach(message_image)

    stp = smtplib.SMTP()
    stp.connect(mail_host, 25)  
    #this line of code can print every single details of connection with server
    #comment it if unnecessary
    stp.set_debuglevel(1)
    stp.login(mail_sender,mail_license)
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("welcome Email successfully sent")
    stp.quit()

def send_support_email(input_text):
    #SMTP server, use 163 mailbox
    mail_host = "smtp.163.com"
    #sender(us) email
    mail_sender = "MyRecipeOfficial@163.com"
    mail_license = "AKZSQAFMQTBPWEOC"
    #Addressee email
    mail_receivers = mail_sender

    mm = MIMEMultipart('related')

    #4.email heading parts
    subject_content = "MyRecipe [Support]"
    mm["From"] = f"sender_name<{mail_sender}>"
    mm["To"] = f"receiver_name<{mail_receivers}>"
    #theme
    mm["Subject"] = Header(subject_content,'utf-8')

    #5.email text
    body_content = input_text
    message_text = MIMEText(body_content,"plain","utf-8")
    mm.attach(message_text)


    #6.add a image
    image_data = open('website/static/Images/maxresdefault.jpeg','rb')
    message_image = MIMEImage(image_data.read())
    image_data.close()
    mm.attach(message_image)

    stp = smtplib.SMTP()
    stp.connect(mail_host, 25)  
    #this line of code can print every single details of connection with server
    #comment it if unnecessary
    stp.set_debuglevel(1)
    stp.login(mail_sender,mail_license)
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("support Email successfully sent")
    stp.quit()