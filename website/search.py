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
from .models import Users, Recipes, IngredientList, Ingredient, Contents, Recipestep, Profiles


search = Blueprint('search', __name__)
CORS(search)

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAQNR7WVADC7MX2ZEW',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='comp3900-w18b-sheeesh'

searchInput = ""

#global variables use to save filters
IngredientFilter = []
MethodFilter = []
SortBy = ""

@search.route('/search_result', methods=['GET','POST'])  
def search_result():
    global IngredientFilter
    global searchInput
    global SortBy

    if request.method == 'POST':
        search_input = request.form.get('Search')
        if search_input is not None:
            if len(search_input) < 1:
                flash("search input can not be empty!")
            else:
                searchInput = search_input  #put into global variable
                reset_all()
                print("reset")
                print(SortBy)
            print(search_input)

        
        #find the query based on search_input
        query = find_query_by_name(searchInput)
        print(f"query = {query}")

        #ingredient filter
        addIngre = request.form.get('IngreAdd') 
        if addIngre is not None: #if None means not clicked, not None means clicked
            IngredientFilter.clear()
            print("Add Ingredient!")
            salt = request.form.get('Salt')
            pepper = request.form.get('Pepper')
            if salt is None and pepper is None:
                flash("ingredient can't be None")
            else:
                IngredientFilter = []
                #add every ingredient filter selected into a list
                if salt is not None:
                    IngredientFilter.append(salt)
                if pepper is not None:
                    IngredientFilter.append(pepper)
                #remove duplicate
                IngredientFilter = list(dict.fromkeys(IngredientFilter))
        else:
            print("Did not add ingredient")

        #SortBy
        SortAdd = request.form.get('SortAdd')
        if SortAdd is not None:
            SortBy = request.form.get('Sort')
            if SortBy is None:
                flash("Sort By can't be None")
            else:
                print(SortBy)
        else:
            print("No sortBy filter")


        #use IngredientFilter for query
        query = use_IngredientFilter_for_query(query)
        #user SortBy (trim orders)
        query = sort_query(query)

        Contents = generate_str_from_list()
        if len(Contents) < 1:
            Contents = "None"
        if len(query) > 0:
            return render_template("search.html",user = current_user,
                search_input = searchInput,query = query,search_value = searchInput,
                contents = Contents)
    message = "No Recipe be Founded"
    return render_template("search.html",user = current_user,search_input = search_input,message = message, contents = Contents)
    


#####helper functions#######

def find_query_by_name(recipeName):
    query = Recipes.query.filter_by(name = recipeName).all()
    return query

#generate str from 2 lists --> IngredientFilter, MethodFilter
#and SortBY
def generate_str_from_list():
    Contents = ""
    for i in IngredientFilter:
        Contents += (f"<< {i} ")
    for m in MethodFilter:
        Contents += (f"<< {m}")
    if len(SortBy) > 0:
        Contents += (f"   <<< Order By  {SortBy}")
    return Contents

def use_IngredientFilter_for_query(query):
    query_after = []
    for q in query:
        find = 0
        ingre = Ingredient.query.filter_by(recipe_id = q.id).all()
        for ing in ingre:
            for i in IngredientFilter:
                print(ing.ingredient)
                print(f"iiii   {i}")
                if ing.ingredient == i:
                    find += 1
                    break
        if find == len(IngredientFilter):
            #add to query_after
            query_after.append(q)
    return query_after

# custom functions to get recipe info
def get_recipe_id(q):
    return q.id

def sort_query(query):
    print("sort_query")
    print(SortBy)
    if SortBy == "DateNew":
        #recently realesed
        query.sort(key = get_recipe_id)
        print(f"New {query}")
    if SortBy == "DateOld":
        #least recently released
        query.sort(key = get_recipe_id, reverse=True)
        print(f"Old {query}")
    return query

#do the rest for each filter when search input have been changed
def reset_all():
    global IngredientFilter
    global searchInput
    global SortBy
    IngredientFilter.clear()
    MethodFilter.clear()
    SortBy = ""