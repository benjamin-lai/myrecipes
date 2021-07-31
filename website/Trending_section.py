# Homepage
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import  current_user, login_required
from flask_cors import CORS
from website import create_app

from flask import Flask

from .models import Profiles
 
#from gi.repository import Gtk
from werkzeug.utils import secure_filename
from .models import Recipes, Contents
from .review import create_comment, retrieve_comments, get_rating
from . import db
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import and_
import boto3
from datetime import datetime
from psycopg2.extensions import AsIs
import json

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='comp3900-w18b-sheeesh'



UPLOAD_FOLDER = 'C:\comp3900\project_data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

trending_section = Blueprint('trending_section', __name__)
CORS(trending_section)

Savelist = {}
Savelist["Day_or_week"] = "Week"
Savelist["type"] = "all"

class Card:
    def __init__(self, recipe, url):
        self.recipe = recipe
        self.url = url

# Filter trending by day or week
@trending_section.route('/Trending filter', methods = ['GET','POST'])
def trending_filter():
    if request.method == "POST":
        filter = json.loads(request.data)
        
        Savelist["Day_or_week"] = filter['filter']
        if Savelist["type"] == "all":
            return redirect(url_for('trending_section.trending_sections'))
        elif Savelist["type"] == "Starter":
            return redirect(url_for('trending_section.Trending_Section.Starter'))
        elif Savelist["type"] == "Dessert":
            return redirect(url_for('recipes.Trending_Section.Dessert'))
        elif Savelist["type"] == "Main":
            return redirect(url_for('recipes.Trending_Section.Main'))
        elif Savelist["type"] == "Snack":
            return redirect(url_for('recipes.Trending_Section.Snack'))
        elif Savelist["type"] == "Breakfast":
            return redirect(url_for('recipes.Trending_Section.Breakfast'))
        elif Savelist["type"] == "Drink":
            return redirect(url_for('recipes.Trending_Section.Drink'))

@trending_section.route('/Trending Section', methods = ['GET','POST'])
def trending_sections():
    Savelist["type"] = "all"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('trending_section.Trending_Section'))
    recipes = Recipes.query.order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    print(Savelist["Day_or_week"])
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)

    return render_template("trending_section.html", query=trending, type="recent", meal_type = "All types", Day_or_week = Savelist["Day_or_week"])

@trending_section.route('/Trending Section.Starter', methods = ['GET','POST'])
def trending_section_Starter():
    Savelist["type"] = "Starter"
    choose = request.form.get('choose')
    if choose:
        return redirect(url_for('trending_section.Trending Section.Starter'))

    recipes = Recipes.query.filter_by(meal_type = "Starter").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Starter", Day_or_week = Savelist["Day_or_week"])
    
@trending_section.route('/Trending Section.Main', methods = ['GET','POST'])
def trending_section_Main():
    Savelist["type"] = "Main"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('recipes.Trending Section.Main'))

    recipes = Recipes.query.filter_by(meal_type = "Main").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Main", Day_or_week = Savelist["Day_or_week"])

@trending_section.route('/Trending Section.Dessert', methods = ['GET','POST'])
def trending_section_Dessert():
    Savelist["type"] = "Dessert"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('recipes.Trending Section.Dessert'))

    recipes = Recipes.query.filter_by(meal_type = "Dessert").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Dessert", Day_or_week = Savelist["Day_or_week"])

@trending_section.route('/Trending Section.Snack', methods = ['GET','POST'])
def trending_section_Snack():
    Savelist["type"] = "Snack"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('recipes.Trending Section.Snack'))

    recipes = Recipes.query.filter_by(meal_type = "Snack").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Snack", Day_or_week = Savelist["Day_or_week"])

@trending_section.route('/Trending Section.Breakfast', methods = ['GET','POST'])
def trending_section_Breakfastk():
    Savelist["type"] = "Breakfast"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('recipes.Trending Section.Breakfast'))

    recipes = Recipes.query.filter_by(meal_type = "Breakfast").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Breakfastk", Day_or_week = Savelist["Day_or_week"])

@trending_section.route('/Trending Section.Drink', methods = ['GET','POST'])
def trending_section_Drink():
    Savelist["type"] = "Drink"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('recipes.Trending Section.Drink'))

    recipes = Recipes.query.filter_by(meal_type = "Drink").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    current_date = datetime.date(datetime.now())
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            if Savelist["Day_or_week"] == 'Day':
                if (i.creation_date - current_date).days <= 1:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
            else:
                if (i.creation_date - current_date).days <= 7:
                    creator_name = i.creator.split(" ")
                    profile = Profiles.query.filter_by(owns = i.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                    card = Card(i, profile.custom_url)
                    trending.append(card)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Drink", Day_or_week = Savelist["Day_or_week"])

