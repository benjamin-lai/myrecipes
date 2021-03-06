# Trending section, for the tab trending section for the second navbar
#  Filters through all of our recipes and sorts them based on the highest number of likes
#   as well as the time period that users have selected.
from flask import Blueprint, render_template, request, redirect, url_for
from flask_cors import CORS
from flask import Flask
from .models import Profiles
from .models import Recipes
from datetime import datetime
import json


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
        if filter['filter']:
            Savelist["Day_or_week"] = filter['filter']
        if Savelist["type"] == "all":
            return redirect(url_for('trending_section.trending_sections'))
        elif Savelist["type"] == "Starter":
            return redirect(url_for('trending_section.trending_section_Starter'))
        elif Savelist["type"] == "Dessert":
            return redirect(url_for('trending_section.trending_section_Dessert'))
        elif Savelist["type"] == "Main":
            return redirect(url_for('trending_section.trending_section_Main'))
        elif Savelist["type"] == "Snack":
            return redirect(url_for('trending_section.trending_section_Snack'))
        elif Savelist["type"] == "Breakfast":
            return redirect(url_for('trending_section.trending_section_Breakfast'))
        elif Savelist["type"] == "Drink":
            return redirect(url_for('trending_section.trending_section_Drink'))

# Trending Section for the recipes with all types
@trending_section.route('/Trending Section', methods = ['GET','POST'])
def trending_sections():
    Savelist["type"] = "all"
    choose = request.form.get('choose')
    if choose:
        redirect(url_for('trending_section.Trending_Section'))
    recipes = Recipes.query.order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
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

    return render_template("trending_section.html", query=trending, type="recent", meal_type = "All types", Day_or_week = Savelist["Day_or_week"])

# Trending recipe for starter
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

# Trending recipe for main   
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

# Trending recipe for dessert 
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

# Trending recipe for snack
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

# Trending recipe for breakfast
@trending_section.route('/Trending Section.Breakfast', methods = ['GET','POST'])
def trending_section_Breakfast():
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

# Trending recipe for drinks
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

