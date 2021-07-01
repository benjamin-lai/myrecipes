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
from .models import Images, Users, Recipes, IngredientList, Ingredient
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
Savelist["Number"] = None
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
    recipe_data = Recipes.query.filter_by(name="6").first()
    print(recipe_data.id)
    image = base64.b64encode(recipe_data.photo).decode('ascii')
    ingredient_data = Ingredient.query.filter_by(recipe_id=recipe_data.id).first()
    print("haha")
    
    button1 = request.form.get('edit_recipe')
    print(button1)
    if button1 != None:
        print("nana")
        print(button1)

        return render_template("edit_recipe.html", user=current_user)
    print("return recipe")
    return render_template("recipe.html", user=current_user, name="6", data=list, image=image, Descriptions=recipe_data.description, RecipeName = 1, MyIngredient = ingredient_data.ingredient)


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
    return render_template("edit_recipe.html", user=current_user)

@views.route('/Create recipe', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        print("in create recipe")
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



        #root = tkinter.Tk()
        #root.withdraw()

        # Message Box
        #messagebox.showinfo("Title", "Message")
    #file = request.form.get('file')
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
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
            # Pass both item ID and image file data to a function
            #SaveToDatabase(id_item, file)
            print("print file below")
            ##print(file.read())
            print("print file above")
            image_datas=file.read()
            Savelist["image_datas"] = image_datas

            '''
            image_newFile=Images(
                image_name=filename,
                username="User 4",
                image_data=image_datas
            )
            db.session.add(image_newFile)
            db.session.commit()

            recipe_newFile=Recipe(
                name = recipe_name,
                description = discriptions,
                image = file.read(),
                creates = serving
            )
            
            db.session.add(recipe_newFile)
            db.session.commit()
            '''
            ##################
            #return render_template("recipe.html", user=current_user)

    
    button3 = request.form.get('button3')
    label = 0
    if button3 != None:
        recipe = Recipes.query.filter_by(name= Savelist["RecipeName"]).first()
        if recipe == None:


            #messagebox.showwarning(title="lalala", message="lalala")
            #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
            
            #return render_template("recipe.html", user=current_user)
        #if label == 1:
            #Mbox('Your title', 'Your text', 1)


        #print(button3)
        #file_data = Images.query.filter_by(username="User 3").first()

          #check not empty, create recipe
            if Savelist["RecipeName"] and Savelist["Description"] and Savelist["Serving"] and Savelist["image_datas"]:
                create_recipe(Savelist["RecipeName"],Savelist["Description"],Savelist["Serving"],Savelist["image_datas"])
                #once click submit, add all from IngredientList to db and assign a recipe id
                recipe_id = Recipes.query.filter_by(name= Savelist["RecipeName"]).first().id
                #add_ingredient_to_db(recipe_id)
                new_ingredient = Ingredient(recipe_id = recipe_id, dosage = Savelist["Dosage"], unit_name = Savelist["UnitName"],
                ingredient = Savelist["MyIngredient"])
                db.session.add(new_ingredient)
                db.session.commit()   
            if Savelist["Dosage"] and Savelist["UnitName"] and Savelist["MyIngredient"]:
                #add ingredients
                add_ingredients_to_list(Savelist["Dosage"],Savelist["UnitName"],Savelist["MyIngredient"])
                
            



            image = base64.b64encode(image_datas).decode('ascii')


            print(Savelist["Serving"])
            print(Savelist["Number"])
            print(Savelist["Dosage"])
            print(Savelist["Description"])
            return render_template("recipe.html", user=current_user, data=list, image=image, Descriptions=Savelist["Description"], RecipeName = Savelist["RecipeName"], MyIngredient = Savelist["MyIngredient"], Step_number = Savelist["Step_number"])
        else:
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
    

        #return render_template("recipe.html", user=current_user)
    
    return render_template("create_recipe.html", user=current_user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def create_recipe (RecipeName, Description, Serving, Photo):
    print(RecipeName)
    print(Description)
    print(Serving)
    #add name and description to db
    print("Begin to add to recipe table")
    new_recipe = Recipes(name = RecipeName, description = Description, photo = Photo, #example only
        serving = Serving, creates = 1)
    db.session.add(new_recipe)
    db.session.commit()             # Commits changes
    print("added successful")
    

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