# Homepage
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Profiles, Newsfeeds


newsfeed = Blueprint('newsfeed', __name__)
CORS(newsfeed)


# default is date, then like, then time, by the spec
@newsfeed.route('/newsfeed', methods=['GET', 'POST'])
def Newsfeed():
    query = Newsfeeds.query.filter_by(contains=current_user.id).order_by(Newsfeeds.creation_date.desc()).order_by((Newsfeeds.likes-Newsfeeds.dislikes).desc()).order_by(Newsfeeds.creation_time.desc()).all()
    type = '#'
    if Newsfeeds.query.filter_by(contains=current_user.id).order_by(Newsfeeds.creation_date.desc()).order_by((Newsfeeds.likes-Newsfeeds.dislikes).desc()).order_by(Newsfeeds.creation_time.desc()).count() == 0:
        type = 'empty'
    return render_template("newsfeed.html", user=current_user, query=query, type=type)


# just by date and time
@newsfeed.route('/newsfeed/recent', methods=['GET', 'POST'])
def Newsfeed_Recent():
    query = Newsfeeds.query.filter_by(contains=current_user.id).order_by(Newsfeeds.creation_date.desc()).order_by(Newsfeeds.creation_time.desc()).all()

    return render_template("newsfeed.html", user=current_user, query=query, type="recent")

# just by likes
@newsfeed.route('/newsfeed/likes', methods=['GET', 'POST'])
def Newsfeed_Likes():
    query = Newsfeeds.query.filter_by(contains=current_user.id).order_by((Newsfeeds.likes-Newsfeeds.dislikes).desc()).all()
    
    return render_template("newsfeed.html", user=current_user, query=query, type="likes")

