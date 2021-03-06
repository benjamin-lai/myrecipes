# Search Page, users can use filters such as ingredient, method, meal type and to sort by.
#  An addition feature is the ingredients filter which allows users to spare ingredients which
#  when they have extra ingredients left.

from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from flask_cors import CORS
from .models import Recipes, Ingredient, Method, Profiles


search = Blueprint('search', __name__)
CORS(search)


searchInput = ""

#global variables use to save filters
IngredientFilter = []
IngredientExclude = []
MethodFilter = []
MealTypeFilter = None
SortBy = None
query = []

@search.route('/search_result', methods=['GET','POST'])  
def search_result():
    global IngredientFilter
    global IngredientExclude
    global searchInput
    global SortBy
    global MethodFilter
    global MealTypeFilter
    global query

    if request.method == 'POST':
        search_input = request.form.get('Search')
        if search_input is not None:
            if len(search_input) < 1:
                #if not searching, display every recipes in database
                query = Recipes.query.all()
                searchInput = ""
            else:   #valid content
                searchInput = search_input #put into global variable
                reset_all()
                
                #split str by space, search them all and put into query
                res = " " in searchInput
                if res is True: #contain space
                    data = searchInput.split()
                    query = []
                    for d in data:
                        #use function for partial search
                        query_temp = find_query_by_partial_search(d)
                        for q in query_temp:
                            query.append(q)
                else:
                    #find the query based on search_input
                    query = find_query_by_partial_search(searchInput)
        else:
            #if not searching, display every recipes in database
                query = Recipes.query.all()
                searchInput = ""

        #drop duplicate
        query = list(dict.fromkeys(query))

        #clear filters
        clear = request.form.get('clear')
        if clear is not None:
            reset_all()
            #go back to same search page without any filters
            #find the query based on search_input
            if len(searchInput) < 1:
                query = Recipes.query.all()
            else:
                query = find_query_by_name(searchInput)
            

            #append profile id into query
            query = append_profile_id(query)
            return render_template("search.html",user = current_user,
                search_input = searchInput,query = query,search_value = searchInput,queryLen = len(query))
        
    
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



        #ingredient search filter
        button_include = request.form.get('include_add')
        button_exclude = request.form.get('exclude_add')
        ingre_include = request.form.get('include')
        ingre_exclude = request.form.get('exclude')
        if button_include is not None:
            #add ingredient include filter
            if len(ingre_include) > 0:
                #split str by space, search them all and put into query
                res = " " in ingre_include
                if res is True: #contain space
                    data = ingre_include.split()
                    for d in data:
                        #add to ingredient filter list
                        IngredientFilter.append(d)
                else:
                    IngredientFilter.append(ingre_include)
            else:
                flash("Ingredient Input can't be empty", category='error')
        if button_exclude is not None:
            #add ingre exclude
            if len(ingre_exclude) > 0:
                #split str by space, search them all and put into query
                res = " " in ingre_exclude
                if res is True: #contain space
                    data = ingre_exclude.split()
                    for d in data:
                        #add to ingredient filter list
                        IngredientExclude.append(d)
                else:
                    IngredientExclude.append(ingre_exclude)
            else:
                flash("Ingredient Exclude can't be empty", category='error')

        #remvoe duplicate for include and exclude
        IngredientFilter = list(dict.fromkeys(IngredientFilter))
        IngredientExclude = list(dict.fromkeys(IngredientExclude))

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

        #MealType filter
        addType = request.form.get('TypeAdd')
        if addType is not None:
            MealTypeFilter = request.form.get('Type')
            if MealTypeFilter is None:
                flash("Meal Type can't be empty", category='error')


        
        #SortBy
        SortAdd = request.form.get('SortAdd')
        if SortAdd is not None:
            SortBy = request.form.get('Sort')
            if SortBy is None:
                flash("Sort By can't be None", category='error')

        #use IngredientFilter for query
        query = use_IngredientFilter_for_query(query)
        #use MethodFilter for query
        query = use_MethodFilter_for_query(query)
        #use MealTypeFilter for query
        query = use_TypeFilter_for_query(query)
        #user SortBy (trim orders)
        query = sort_query(query)
        #use exclude ingredient filter
        query = use_ingredient_exclude_filter(query)
        
        include_contents = generate_include_contents()
        exclude_contents = generate_exclude_contents()
        Contents = generate_str_from_list()
        if len(Contents) < 1:
            Contents = ""
        if len(query) > 0:
            #append profile id into query
            query = append_profile_id(query)
            return render_template("search.html",user = current_user,
                search_input = searchInput,query = query,search_value = searchInput,
                contents = Contents, include_ingreList = include_contents,queryLen = len(query),
                exclude_ingreList = exclude_contents)
        else:
            message = f"No Recipe be Founded  {searchInput}"
            return render_template("search.html",user = current_user,
                search_input = searchInput,query = query,search_value = searchInput,
                contents = Contents, include_ingreList = include_contents, 
                exclude_ingreList = exclude_contents,message = message,queryLen = len(query))
    else:
        #if not searching, display every recipes in db
        query = Recipes.query.all()
        searchInput = ""
        message = ""
        if len(query) < 1:
            message = f"No Recipe be Founded  {searchInput}"
        #append profile id into query
        query = append_profile_id(query)
        return render_template("search.html",user = current_user,search_input = searchInput
            ,message = message,queryLen = len(query),query = query)
    


#####helper functions#######
def find_query_by_name(recipeName):
    result = []
    query = Recipes.query.all()
    for q in query:
        if q.name.lower() == recipeName.lower():
            result.append(q)
    return result

#partial search
def find_query_by_partial_search(recipeName):
    result = []
    query = Recipes.query.all()
    for q in query:
        if (recipeName.lower() in q.name.lower()) or (recipeName.lower() == q.name.lower()):
            result.append(q)
    return result

#find which elements of ingredients have been seleceted, and add them to list
def check_and_add_ingredient(Pork,Beef,Vegi,SeaFood,Poultry):
    global IngredientFilter
    if Pork is None and Beef is None and Vegi is None and SeaFood is None and Poultry is None:
        flash("Ingredient can't be None", category='error')
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
        flash("Method can't be None", category='error')
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
    if MealTypeFilter is not None:
        Contents += (f"<< {MealTypeFilter}")
    if SortBy is not None:
        Contents += (f"<<< Order By {SortBy}")
    return Contents

def use_IngredientFilter_for_query(query):
    query_after = []
    for q in query:
        find = 0
        ingre = Ingredient.query.filter_by(recipe_id = q.id).all()
        for ing in ingre:
            for i in IngredientFilter:
                if ing.ingredient.lower() == i.lower():
                    find += 1
                    break
        if find == len(IngredientFilter):
            #add to query_after
            query_after.append(q)
    return query_after


def use_ingredient_exclude_filter(query):
    query_after = []
    for q in query:
        flag = 0
        ingre = Ingredient.query.filter_by(recipe_id = q.id).all()
        for ing in ingre:           
            for i in IngredientExclude:
               if ing.ingredient.lower() == i.lower():
                   flag = 1
        if flag == 0:
            query_after.append(q)
    return query_after

def use_MethodFilter_for_query(query):
    query_after = []
    for q in query:
        find = 0
        method = Method.query.filter_by(recipe_id = q.id).all()
        for me in method:
            for m in MethodFilter:
                if me.method.lower() == m.lower():
                    find += 1
                    break
        if find == len(MethodFilter):
            #add to query_after
            query_after.append(q)
    return query_after

def use_TypeFilter_for_query(query):
    if MealTypeFilter is None:
        return query
    else:
        query_after = []
        for q in query:
            if q.meal_type.lower() == MealTypeFilter.lower():
                query_after.append(q)
        return query_after

# custom functions to get recipe info
def get_recipe_id(q):
    return q.id
def get_like_minus_dislike_num(q):
    return int(q.num_of_likes - q.num_of_dislikes)

def sort_query(query):
    if SortBy == "DateNew":
        #recently realesed
        query.sort(key = get_recipe_id)
    if SortBy == "DateOld":
        #least recently released
        query.sort(key = get_recipe_id, reverse=True)
    #if SortBy == "Star":
        #rate of star, currently disable
    if SortBy == "Likes":
        #like - dislike
        query.sort(key = get_like_minus_dislike_num)
    return query

#do the rest for each filter when search input have been changed
def reset_all():
    global IngredientFilter
    global IngredientExclude
    global searchInput
    global SortBy
    global MethodFilter
    global MealTypeFilter
    IngredientFilter.clear()
    IngredientExclude.clear()
    MethodFilter.clear()
    MealTypeFilter = None
    SortBy = None

def generate_include_contents():
    Contents = ""
    for i in IngredientFilter:
        Contents += (f"<< {i} ")
    return Contents

def generate_exclude_contents():
    Contents = ""
    for i in IngredientExclude:
        Contents += (f"<< {i} ")
    return Contents

#append recipe's creator's profile id after query
def append_profile_id(query):
    recipes = []
    profiles = []
    for r in query:
        recipe = Recipes.query.filter_by(id=r.id).first()
        profile = Profiles.query.filter_by(profile_id=recipe.creates).first()
        setattr(recipe, "custom_url", profile.custom_url)
        recipes.append(recipe)
    return recipes