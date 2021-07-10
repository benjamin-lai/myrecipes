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
from .models import Users, Recipes, Ingredient, Contents, Recipestep, Profiles,Method,Meal_Type


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
MealTypeFilter = ""
SortBy = ""

@search.route('/search_result', methods=['GET','POST'])  
def search_result():
    global IngredientFilter
    global searchInput
    global SortBy
    global MethodFilter
    global MealTypeFilter
    if request.method == 'POST':
        search_input = request.form.get('Search')
        if search_input is not None:
            if len(search_input) < 1:
                flash("search input can not be empty!")
            else:
                searchInput = search_input  #put into global variable
                reset_all()
                print("reset")
                print(MealTypeFilter)
        
        #find the query based on search_input
        query = find_query_by_name(searchInput)
        print(f"query = {query}")

        #ingredient filter
        addIngre = request.form.get('IngreAdd') 
        if addIngre is not None: #if None means not clicked, not None means clicked
            IngredientFilter.clear()
            Pork = request.form.get('pork')
            Beef = request.form.get('beef')
            Vegi = request.form.get('vegetables')
            SeaFood = request.form.get('seafood')
            Poultry = request.form.get('poultry')

            IngreFlag = check_and_add_ingredient(Pork,Beef,Vegi,SeaFood,Poultry)
            if IngreFlag is True: # have ingredient slected
                print("added ingredients")
                print(IngredientFilter)
        else:
            print("Did not add ingredient")


        #Method filter
        addMethod = request.form.get('MethodAdd')
        if addMethod is not None:
            MethodFilter.clear()
            Baking  = request.form.get('baking')
            Frying  = request.form.get('frying')
            Grilling  = request.form.get('grilling')
            Steaming  = request.form.get('steaming')
            Braising  = request.form.get('braising')
            StirFrying  = request.form.get('stir_frying')

            MethodFlag = check_and_add_method(Baking,Frying,Grilling,Steaming,Braising, StirFrying)
            if MethodFlag is True: # have ingredient slected
                print("added methods")
                print(MethodFilter)
        else:
            print("Did not add methods")


        #MealType filter
        addType = request.form.get('TypeAdd')
        if addType is not None:
            MealTypeFilter = request.form.get('Type')
            if MealTypeFilter is None:
                flash("Meal Type can't be empty")
            else:
                print(MealTypeFilter)
        else:
            print("No meal type selected")

        
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
        #use MethodFilter for query
        query = use_MethodFilter_for_query(query)
        #use MealTypeFilter for query
        query = use_TypeFilter_for_query(query)
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

#find which elements of ingredients have been seleceted, and add them to list
def check_and_add_ingredient(Pork,Beef,Vegi,SeaFood,Poultry):
    global IngredientFilter
    if Pork is None and Beef is None and Vegi is None and SeaFood is None and Poultry is None:
        flash("Ingredient can't be None")
        return False
    if Pork is not None:
        IngredientFilter.append(Pork)
    if Beef is not None:
        IngredientFilter.append(Beef)
    if Vegi is not None:
        IngredientFilter.append(Vegi)
    if SeaFood is not None:
        IngredientFilter.append(SeaFood)
    if Poultry is not None:
        IngredientFilter.append(Poultry)
    #remove duplicate
    IngredientFilter = list(dict.fromkeys(IngredientFilter))  
    return True

def check_and_add_method(Baking,Frying,Grilling,Steaming,Braising, StirFrying):
    global MethodFilter
    if Baking is None and Frying is None and Grilling is None and Steaming is None and Braising is None and StirFrying is None:
        flash("Method can't be None")
        return False
    if Baking is not None:
        MethodFilter.append(Baking)
    if Frying is not None:
        MethodFilter.append(Frying)
    if Grilling is not None:
        MethodFilter.append(Grilling)
    if Steaming is not None:
        MethodFilter.append(Steaming)
    if Braising is not None:
        MethodFilter.append(Braising)
    if StirFrying is not None:
        MethodFilter.append(StirFrying)
    #remove duplicate
    MethodFilter = list(dict.fromkeys(MethodFilter))
    return True

#generate str from 3 lists --> IngredientFilter, MethodFilter, MealTypeFilter
#and SortBY
def generate_str_from_list():
    Contents = ""
    for i in IngredientFilter:
        Contents += (f"<< {i} ")
    for m in MethodFilter:
        Contents += (f"<< {m}")
    if len(MealTypeFilter) > 0:
        Contents += (f"<< {MealTypeFilter}")
    if len(SortBy) > 0:
        Contents += (f"<<< Order By {SortBy}")
    return Contents

def use_IngredientFilter_for_query(query):
    query_after = []
    for q in query:
        find = 0
        ingre = Ingredient.query.filter_by(recipe_id = q.id).all()
        for ing in ingre:
            for i in IngredientFilter:
                print(ing.ingredient)
                if ing.ingredient.lower() == i.lower():
                    find += 1
                    break
        if find == len(IngredientFilter):
            #add to query_after
            query_after.append(q)
    return query_after

def use_MethodFilter_for_query(query):
    query_after = []
    for q in query:
        find = 0
        method = Method.query.filter_by(recipe_id = q.id).all()
        for me in method:
            for m in MethodFilter:
                print(me.method)
                if me.method.lower() == m.lower():
                    find += 1
                    break
        if find == len(MethodFilter):
            #add to query_after
            query_after.append(q)
    return query_after

def use_TypeFilter_for_query(query):
    if len(MealTypeFilter) < 1:
        return query
    query_after = []
    for q in query:
        print(f"type : {q.meal_type}")
        if q.meal_type.lower() == MealTypeFilter.lower():
            query_after.append(q)
    return query_after

# custom functions to get recipe info
def get_recipe_id(q):
    return q.id
def get_like_minus_dislike_num(q):
    return int(q.num_of_likes - q.num_of_dislikes)

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
    #if SortBy == "Star":
        #rate of star, currently disable
    if SortBy == "Likes":
        #like - dislike
        query.sort(key = get_like_minus_dislike_num)
    return query

#do the rest for each filter when search input have been changed
def reset_all():
    global IngredientFilter
    global searchInput
    global SortBy
    global MethodFilter
    global MealTypeFilter
    IngredientFilter.clear()
    MethodFilter.clear()
    MealTypeFilter = ""
    SortBy = ""