# Homepage
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
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
from .models import StarredRecipes, Users, Recipes, Ingredient, Contents, Recipestep, Profiles, Method, History, Likes, Comments, Cookbooks, Cookbooks_lists
from .review import create_comment, retrieve_comments, get_rating
from . import db
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import and_
import base64
import boto3
import random
from datetime import datetime
import psycopg2
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

historys = Blueprint('history', __name__)
CORS(historys)

class Card:
    def __init__(self, recipe, url):
        self.recipe = recipe
        self.url = url

@historys.route('/history', methods = ['GET','POST'])
def history():
    
    if current_user.is_authenticated:    
        histories = History.query.filter_by(userid = current_user.id).order_by(History.last_view_date.desc(), History.last_view_time.desc()).all()
        query = []
        for i in histories:
            print(i.last_view_date)
            print(i.last_view_time)
            recipes = Recipes.query.filter_by(id = i.recipe).all()
            for recipe in recipes:
                # Link the creator's name as url
                creator_name = recipe.creator.split(" ")
                profile = Profiles.query.filter_by(owns = recipe.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
                card = Card(recipe, profile.custom_url)
                query.append(card)
    else:
        return render_template("restricted_access.html")
    
    
    
    
    conn = psycopg2.connect(
    database="rec", user='postgres', password='aa', host='localhost', port= '5432'
)
    conn.autocommit = True
    cursor = conn.cursor()
    # i1 is the history of the curr user joined with ingredients to see what ingredients their history has.
    # i2 is a list of recipes that have ingredients which arent in the i1 list.
    # i1 is joined with i2 so it can find a list of recipes which use the same ingredients or ingredients with similar names as the ones in their history, but dont contain any of the
    # recipes that are already in their recipe, where it counts the amount of times that a recipe has the same ingredients as the previous recipes.
    # meaning if recipe 1 and recipe 2 have 3 ingredients in common or ingredients that are similar then it will count that
    # this list is called s1 and then unioned with another list which is basically the same as s1 but the regex is the opposite way to ensure
    # that it takes cases that are missed by s1, ex. 'chicken' is like 'chicken wing' but 'chicken wing' is not like 'chicken'
    # then that joined list is called s2 and that is joined with recipes to find the name and photo of the recipes, where it is order by highest to
    # lowest count of similar ingredients, then those with highest ingredients is displayed first.
    
    
    # tldr: count amount of similar ingredients of other recipes then display the ones with the highest similar ingredients.
    sql ='''select s2.recipe_id, count(*), name, photo
            from
                (select * from
                    (select * from
                        (select distinct ingredient
                            from history h
                            join ingredient i on i.recipe_id = h.recipe
                            where userid=5) i1
                        inner join
                            (select recipe_id, ingredient from Ingredient
                            except
                            
                            select recipe_id, ingredient
                            from history h
                            join ingredient i on i.recipe_id = h.recipe
                            where userid=5) i2
                            
                        on lower(concat('%%', i1.ingredient, '%%')) like lower(concat( '%%', i2.ingredient, '%%'))) s1     
                union
                    (select * from
                        (select distinct ingredient
                            from history h
                            join ingredient i on i.recipe_id = h.recipe
                            where userid=5) i1
                        inner join
                            (select recipe_id, ingredient from Ingredient
                            except
                             
                            select recipe_id, ingredient
                            from history h
                            join ingredient i on i.recipe_id = h.recipe
                            where userid=5) i2
                            
                        on lower(concat('%%', i2.ingredient, '%%')) like lower(concat( '%%', i1.ingredient, '%%')))) s2
                
                    
        join recipes r 
            on r.id = s2.recipe_id
        group by s2.recipe_id, r.name, r.photo
        order by count desc
        limit 4;
        '''
    
    id = str(current_user.id)
    
    cursor.execute(sql, (id, id))
    res=cursor.fetchall()
    
    
    return render_template("history.html", query=query, type="recent", res=res)

@historys.route('/delete history', methods=['GET', 'POST'])
def delete_history():
    if request.method == 'POST':
        browsing_history = json.loads(request.data)
        print(request.data)
        print(browsing_history)

        recipeId = browsing_history['id']
        print("recipeId: ", recipeId)
        delete_histories = History.query.filter_by(userid = current_user.id, recipe = recipeId).first()
        db.session.delete(delete_histories)
        db.session.commit()
        histories = History.query.filter_by(userid = current_user.id).order_by(History.last_view_time.asc()).all()
        query = []
        for i in histories:
            recipes = Recipes.query.filter_by(id = i.recipe).all()
            for j in recipes:
                query.append(j)
        return redirect(url_for('recipes.history'))
