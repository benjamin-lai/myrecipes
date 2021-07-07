# Homepage
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Profiles, Newsfeeds


newsfeed = Blueprint('newsfeed', __name__)
CORS(newsfeed)

@newsfeed.route('/newsfeed', methods=['GET', 'POST'])
def Newsfeed():
    query = Newsfeeds.query.filter_by(contains=current_user.id).order_by(Newsfeeds.id.desc()).all()
    
    return render_template("newsfeed.html", user=current_user, query=query, type="recent")




@newsfeed.route('/newsfeed/likes', methods=['GET', 'POST'])
def Newsfeed_Likes():
    query = Newsfeeds.query.filter_by(contains=current_user.id).order_by(Newsfeeds.likes.desc()).all()
    
    return render_template("newsfeed.html", user=current_user, query=query, type="likes")

