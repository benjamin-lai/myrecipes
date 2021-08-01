# Profile Page, I haven't done anything that cool yet.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Recipes, Ingredient, Contents, Recipestep, Method,Meal_Type, Profiles, Cookbooks, Cookbooks_lists


cookbook = Blueprint('cookbook', __name__)
CORS(cookbook)

#cookbook center in profile
@cookbook.route('/cookbook', methods=['GET','POST'])  
def cook_book():
    #user can only view the recipe of their own
    cookbook_all = Cookbooks.query.filter_by(contains = current_user.id).all()
    if current_user.is_authenticated:
        return render_template("cookbook.html", user = current_user, books = cookbook_all)
    else:
        flash("Only logged in user can view cookbook", category="error")
        return redirect(url_for('/'))

#cookbook
@cookbook.route('/cookbook.<book_name>.<int:book_id>', methods=['GET','POST'])  
def cook_book2(book_name,book_id):
    #check avaliablity of name and id
    #allowed user who is not the creator to view
    cookbook = Cookbooks.query.filter_by(name = book_name, id = book_id).first()
    if cookbook is None:
        flash("No cookbook exists with this name and id.", category="error")
        return redirect(url_for('views.home'))

    #show recipe in cookboook
    cookbook_list = Cookbooks_lists.query.filter_by(cookbook_id = book_id).all()
    recipe_list = []
    for book in cookbook_list:
        recipe = Recipes.query.filter_by(id = book.recipe_id).first()
        recipe_list.append(recipe)

    #no recipe inside
    if len(recipe_list) < 1:
        empty = True
    else:
        empty = False
    if current_user.is_authenticated:
        recipe_list = append_profile_id(recipe_list)
        return render_template("cookbook_content.html",user = current_user, empty = empty, recipe_list = recipe_list, 
             cookbook = cookbook)
    else:
        flash("Only logged in user can view cookbook", category="error")
        return redirect(url_for('views.home'))

#helper func
#put custom url into recipe list
def append_profile_id(query):
    recipes = []
    profiles = []
    for r in query:
        recipe = Recipes.query.filter_by(id=r.id).first()
        profile = Profiles.query.filter_by(profile_id=recipe.creates).first()
        setattr(recipe, "custom_url", profile.custom_url)
        recipes.append(recipe)
    return recipes