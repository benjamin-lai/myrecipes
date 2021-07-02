# Homepage
from flask import Blueprint, render_template, request, flash, redirect, url_for
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
from .models import Users, Recipes, IngredientList, Ingredient, Contents, Recipestep
from . import db

import base64



UPLOAD_FOLDER = 'C:\comp3900\project_data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint('views', __name__)
CORS(views)


Savelist = {}
Savelist["Serving"] = None
Savelist["RecipeName"] = None
Savelist["RecipeId"] = None
Savelist["Dosage"] = None
Savelist["UnitName"] = None
Savelist["MyIngredient"] = None
Savelist["Description"] = None
Savelist["image_datas"] = None
Savelist["Step_number"] = None

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/recipe', methods = ['GET','POST'])
def recipe():
    recipe_id = request.form.get('recipe_id')
    print(f"recipe id is  {recipe_id}")
    recipe_data = Recipes.query.filter_by(name="6").first()
    print(recipe_data.id)
    ingredient_data = Ingredient.query.filter_by(recipe_id=recipe_data.id).first()
    print("haha")
    
    button1 = request.form.get('edit_recipe')
    print(button1)
    if button1 != None:
        print("nana")
        print(button1)

        return render_template("edit_recipe.html", user=current_user)
    print("return recipe")
    
    #delete this recipe
    deletebutton = request.form.get('Delete_recipe')
    print(f"this is delete   !!{deletebutton}")
    if deletebutton != None:
        print("nanananna")
        #delete recipe
        obj = Recipes.query.filter_by(id = recipe_id).first()
        name = obj.name
        db.session.delete(obj)
        #delete step
        obj = Recipestep.query.filter_by(recipe_id = recipe_id).all()
        for o in obj:
            db.session.delete(obj)
        #delete ingredients
        obj = Ingredient.query.filter_by(recipe_id = recipe_id).all()
        for o in obj:
            db.session.delete(obj)
        db.session.commit()
        print("finish delete")
        return render_template("delete_recipe.html",user = current_user, recipe_id = recipe_id, name = name)
    else:
        return render_template("recipe.html", user=current_user, name="6", Descriptions=recipe_data.description)
"""
@views.route('/edit recipe', methods = ['GET', 'POST'])
def edit_recipe():
    #add a clear button to the step no. of ingredients
    #add a method to clear the step descriptions
"""


@views.route('/edit recipe', methods = ['GET', 'POST'])
def edit_recipe():
    if request.method == 'POST':
        print("in edit recipe")
        button1 = request.form.get('button1')
        if button1 != None:
            print(button1)
            RecipeName = request.form.get('Recipe Name')
            print(RecipeName)
        
            Serving = request.form.get('Servings')
            print(Serving)
            Number = request.form.get('No.')
            print(Number)
            Dosage = request.form.get('unit')
            print(Dosage)
            UnitName = request.form.get('Unit Name')
            print(UnitName)
            MyIngredient = request.form.get('Ingredient Name')
            print(MyIngredient)
            Step_number = request.form.get('step_number')
            print(Step_number)
            
            Savelist["Serving"] = Serving
            Savelist["RecipeName"] = RecipeName
            Savelist["Number"] = Number
            Savelist["Dosage"] = Dosage
            Savelist["UnitName"] = UnitName
            Savelist["MyIngredient"] = MyIngredient

        button2 = request.form.get('button2')
            
        label = 0
        if button2 != None:
            label = 1
            #messagebox.showwarning(title="lalala", message="lalala")
            #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
            print(button2)
            #return render_template("recipe.html", user=current_user)
        #if label == 1:
            #Mbox('Your title', 'Your text', 1)

            print(Savelist["Serving"])
            print(Savelist["Number"])
            print(Savelist["Dosage"])
            Description = request.form.get('discriptions')
            print(Description)
            Savelist["Description"] = Description

    if request.method == 'POST':
        # check if the post request has the file part
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            print("print file below")
            ##print(file.read())
            print("print file above")
            image_datas=file.read()
            Savelist["image_datas"] = image_datas

            
        button3 = request.form.get('button3')

        if button3 != None:
            recipe = Recipes.query.filter_by(name= Savelist["RecipeName"]).first()
            #check not empty, create recipe
            if Savelist["RecipeName"]:
                recipe.name = Savelist["RecipeName"]
            if Savelist["Description"]:
                recipe.description = Savelist["Description"]
            if Savelist["Serving"]:
                recipe.serving = Savelist["Serving"]
            if Savelist["image_datas"]:
                recipe.photo = Savelist["image_datas"]
                
            ingredient = Ingredient.query.filter_by(recipe_id= recipe.id).first()
            if Savelist["Dosage"]:
                ingredient.dosage = Savelist["Dosage"]
            if Savelist["UnitName"]:
                ingredient.unit_name = Savelist["UnitName"]
            if Savelist["MyIngredient"]:
                ingredient.ingredient = Savelist["MyIngredient"]
                
            image = base64.b64encode(recipe.photo).decode('ascii')

            return render_template("recipe.html", user=current_user, data=list, image=image, Descriptions= recipe.description, RecipeName = recipe.name, MyIngredient = ingredient.unit_name)
    return render_template("edit_recipe.html", user=current_user, rname = "chicken", rdes = "no", servingValue = "2")



@views.route('/Create recipe', methods=['GET', 'POST'])
def create_recipe():
    Contents = take_ingredientList_into_str()
    print(IngredientList)
    if request.method == 'POST':
        RecipeName = request.form.get('Recipe Name')
        Description = request.form.get('Recipe Des')
        Serving = request.form.get('Servings')
        Dosage = request.form.get('dosage')
        UnitName = request.form.get('Unit Name')
        MyIngredient = request.form.get('Ingredient Name')
        StepNo = request.form.get('step_number')
        StepDes = request.form.get('discriptions')

        if RecipeName and Description and Serving:  #check not empty, create recipe
            create_recipe(RecipeName,Description,Serving)
            Savelist["RecipeName"] = RecipeName
            flash(f"Create Recipe {RecipeName} Successfully!")

        if check_create(Savelist["RecipeName"],current_user.id) is True:    #is true, already created recipe
            print(f"{Dosage} + {UnitName} + {MyIngredient}")
            if Dosage and UnitName and MyIngredient:
                #we can begin to add ingredients
                add_ingredients_to_list(Dosage,UnitName,MyIngredient)
                Contents = take_ingredientList_into_str()

                flash(f"added ingredient {MyIngredient} successfully!")

            if StepNo and StepDes:
                # we can begin to add steps
                print(f"step + {StepDes}, No. + {StepNo}")
                #get the latest id of this recipeName
                obj = Recipes.query.filter_by(name= Savelist["RecipeName"]).all()
                recipe_id = obj[-1].id
                print("begin to add to db")
                print(f"Step des {StepDes}")
                new_step = Recipestep(recipe_id = recipe_id, step_no = StepNo, step_comment = StepDes)
                db.session.add(new_step)
                db.session.commit()             # Commits changes
                flash(f"Added comment at Step.{StepNo}!")

        else:
            flash(f"Please create the recipe first!")

        Submit = request.form.get('Submit')
        if Submit != None:
            #get the latest id of this recipeName
            obj = Recipes.query.filter_by(name= Savelist["RecipeName"]).all()
            recipe_id = obj[-1].id
            Savelist["RecipeId"] = recipe_id
            add_ingredient_to_db(recipe_id)
            #fetch description from db
            Description = Recipes.query.filter_by(id = recipe_id).first().description
            #fetch steps from db
            Steps = ""
            obj = Recipestep.query.filter_by(recipe_id = recipe_id).all()
            for o in obj:
                Steps += f"Step.{o.step_no} --> {o.step_comment}  \n"
            print("Yeeeeeea")
            return render_template("recipe.html", user=current_user, Descriptions=Description, 
                RecipeName = Savelist["RecipeName"], MyIngredient = Contents,IngreContents = Contents, Steps = Steps, recipe_id = recipe_id)
        else:
            #get the latest id of this recipeName
            obj = Recipes.query.filter_by(name= Savelist["RecipeName"]).all()
            recipe_id = obj[-1].id

            print("NOooooo")
            return render_template("create_recipe.html", user=current_user)

    else:
        return render_template("create_recipe.html", user=current_user)

@views.route('/Delete recipe', methods=['GET', 'POST'])
def delete_recipe():
    #delete the recipe using recipeId
    #recipe_id = request.form.get('recipe_id')
    #Name = Recipes.query.filter_by(id = recipe_id).first().name
    print(f"recipeeeee   idddd is  ")
    print(Savelist["RecipeId"])
    return render_template("delete_recipe.html",user = current_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def create_recipe (RecipeName, Description, Serving):
    #add name and description to db
    print("Begin to add to recipe table")
    new_recipe = Recipes(name = RecipeName, description = Description, 
        serving = Serving, creates = current_user.id)
    db.session.add(new_recipe)
    db.session.commit()             # Commits changes
    print("added successful")

#def add_step (recipe_id, step_no, )
    

#add ingredients to IngredientList
def add_ingredients_to_list(Dosage,UnitName,MyIngredient):
    #put in a dictionary temporary, after the recipe create add the recipe id
    Dict = dict({'Dosage' : Dosage, 'UnitName' : UnitName, 'Ingredient' : MyIngredient})
    IngredientList.append(Dict)
    print(IngredientList)

def add_ingredient_to_db(recipe_id):
    for item in IngredientList:
        Dosage = item.get('Dosage')
        UnitName = item.get('UnitName')
        MyIngredient = item.get('Ingredient')
        print(Dosage)
        print(UnitName)
        print(MyIngredient)
        new_ingredient = Ingredient(recipe_id = recipe_id, dosage = Dosage, unit_name = UnitName,
            ingredient = MyIngredient)
        db.session.add(new_ingredient)
        db.session.commit()             # Commits changes
        print("added successful")
        print(IngredientList)

def take_ingredientList_into_str():
    Contents = ""
    counter = 1
    for item in IngredientList:
        Dosage = item.get('Dosage')
        UnitName = item.get('UnitName')
        MyIngredient = item.get('Ingredient')
        Contents += (f"{counter}. --> {Dosage} {UnitName} {MyIngredient}.     "
                    f" ")
        counter += 1
    return Contents

def check_create(RecipeName,userid):
    print(f"name {RecipeName} + {userid}")
    obj = Recipes.query.filter_by(name= RecipeName, id = userid).first()
    if obj != None:
        return True
    return False
