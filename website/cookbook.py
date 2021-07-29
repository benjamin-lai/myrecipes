# Profile Page, I haven't done anything that cool yet.
from typing import BinaryIO
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_cors import CORS
from . import db
from .models import Users, Profiles, Cookbooks, Cookbooks_lists
import boto3
from werkzeug.utils import secure_filename
from .models import Users, Recipes, Ingredient, Contents, Recipestep, Profiles,Method,Meal_Type


cookbook = Blueprint('cookbook', __name__)
CORS(cookbook)

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='comp3900-w18b-sheeesh'

#cookbook center in profile
@cookbook.route('/cookbook', methods=['GET','POST'])  
def cook_book():
    #user can only view the recipe of their own
    cookbook_all = Cookbooks.query.filter_by(contains = current_user.id).all()
    print(f"all    {cookbook_all}")
    return render_template("cookbook.html",user = current_user, books = cookbook_all)

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

    print(f"recipe list  {recipe_list}")
    #no recipe inside
    if len(recipe_list) < 1:
        empty = True
    else:
        empty = False

    #remove recipes
    return render_template("cookbook_content.html",user = current_user, empty = empty, recipe_list = recipe_list, 
    cookbook = cookbook)