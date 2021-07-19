# Homepage
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  current_user, login_required
from flask_cors import CORS
from website import create_app

from flask import Flask

import os
import tkinter
from tkinter import messagebox
import ctypes 
#from gi.repository import Gtk
from werkzeug.utils import secure_filename
from .models import Users, Recipes, Ingredient, Contents, Recipestep, Profiles
from . import db
from sqlalchemy import desc
from sqlalchemy import func
import base64
import boto3

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='comp3900-w18b-sheeesh'



UPLOAD_FOLDER = 'C:\comp3900\project_data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint('views', __name__)
CORS(views)



@views.route('/', methods=['GET', 'POST'])
def home():
    recipe = Recipes.query.all()
    user = Profiles.query.filter_by(owns = current_user.id).first()
    return render_template("home.html", user=current_user, res = recipe, userName = user.first_name)





