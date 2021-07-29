# Homepage
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  current_user, login_required
from flask_cors import CORS
from website import create_app

from flask import Flask

import os
import ctypes 
#from gi.repository import Gtk
from werkzeug.utils import secure_filename
from .models import StarredRecipes, Recipes, Ingredient, Contents, Recipestep, Profiles, Method, History, Likes, Comments, Cookbooks, Cookbooks_lists
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

recipes = Blueprint('recipes', __name__)
CORS(recipes)

IngredientList = []
Savelist = {}
Savelist["Is_creating"] = False
Savelist["Serving"] = None
Savelist["RecipeName"] = None
Savelist["RecipeId"] = None
Savelist["Dosage"] = None
Savelist["UnitName"] = None
Savelist["MyIngredient"] = None
Savelist["Description"] = None
Savelist["image_datas1"] = None
Savelist["image_datas2"] = None
Savelist["Step_number"] = -1   #step number can't be None
Savelist["Step_Des"] = None
Savelist["image_name2"] = None
Savelist["image_name1"] = None
Savelist["edit_ingredient"] = False
Savelist["already_delete"] = False
Savelist["can't_be_zero"] = False
Savelist["deleting_step"] = False
Savelist["contents"] = ''

Savelist["color_1"] = ''
Savelist["color_2"] = ''
Savelist["color_3"] = ''
Savelist["color_4"] = ''


class ingre:
    def __init__(self, ingredient, order):
        self.ingredient = ingredient
        self.order = order


@recipes.route('/Recipe cards', methods = ['GET','POST'])
def recipe_cards():
    query = Recipes.query.order_by(Recipes.id.desc()).all()
    return render_template("Recipe_card.html", query=query, type="recent")

#for testing now
@recipes.route('/recipes', methods = ['GET','POST'])
def recipe():
    recipe = Recipes.query.all()
    return render_template("test.html",user = current_user)

@recipes.route('/Add discription', methods=['GET', 'POST'])
def add_discription():
    if Savelist["can't_be_zero"] == True:
        flash("At least contain one step discription", 'error')
        Savelist["can't_be_zero"] = False

    StepNo = request.form.get('step_number')
    StepDes = request.form.get('discriptions')
    
    if check_create(Savelist["RecipeName"],current_user.id) is True:    #is true, already created recipe
        current_step = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).first()
        Find = request.form.get('find')
        obj = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).all()
        # We assume there is at last one discription
        Shown_discription = ""
        if obj != []:
            Shown_discription = obj[0]
        
        if Find != None:
            Find_discription = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"], step_no = StepNo).first()
            if Find_discription == None:
                if Savelist["deleting_step"] == True:
                    flash("successfully deleting current step")
                else:
                    flash("Don't create this step yet", 'error')
                Savelist["deleting_step"] = False
            else:
                Shown_discription = Find_discription
            


        upload_images = request.form.get('upload_images')
        if upload_images != None:
            file2 = request.files['file2']
            if file2 != None:
                file_data = file2

                if file2.filename == '':
                    flash('Continue to create recipe')
                    return redirect(request.url)
                if file2 and allowed_file(file2.filename):
                    filename = secure_filename(file2.filename)
                

                    file2.save(filename)
                    s3.upload_file(
                        Bucket = 'comp3900-w18b-sheeesh',
                        Filename=filename,
                        Key = filename
                    )
                    os.remove(filename)
                    image_datas2_read = file_data.read()
                    image2 = base64.b64encode(image_datas2_read).decode('ascii')
                    image_datas2 = image2
                    Savelist["image_name2"] = filename

                    Savelist["Step_number"] = StepNo
                    Savelist["Step_Des"] = StepDes
            no_list = []
            obj = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).all()
            for o in obj:
                no_list.append(int(o.step_no))
                if int(Savelist["Step_number"]) == int(o.step_no):
                    if StepNo:
                        o.step_no = StepNo
                    if StepDes:
                        o.step_comment = StepDes
                    if Savelist["image_name2"]:
                        o.photo = Savelist["image_name2"]
                    db.session.commit()

                    # Set to current step
                    Shown_discription = o

            
            if int(Savelist["Step_number"]) not in no_list:
                if StepNo and StepDes and Savelist["image_name2"]:
                    # we can begin to add steps
                    #get the latest id of this recipeName
                    recipe_id = Savelist["RecipeId"]

                    new_step = Recipestep(recipe_id = recipe_id, step_no = StepNo, step_comment = StepDes, photo = Savelist["image_name2"])
                    db.session.add(new_step)
                    db.session.commit()             # Commits changes
                    # Set to current step
                    Shown_discription = new_step
                    flash(f"Added comment and photo at Step.{StepNo}!")
            else:
                if Savelist["can't_be_zero"] == True:
                    flash("At least contain one step discription", 'error')
                    Savelist["can't_be_zero"] = False
                else:    
                    flash(f"Update comment and photo at Step.{StepNo}!")
        
            Savelist["color_4"] = "red"
            if (Savelist["Step_number"] != -1) and Savelist["Step_Des"] and (Savelist["image_name2"] == None) and (upload_images != None):
                flash(f"Please upload photo for steps!", 'error')
            
            if (Savelist["Step_number"] == -1) and Savelist["Step_Des"] and (Savelist["image_name2"] != None) and (upload_images != None):
                flash(f"Please add Step Number!", 'error')
                
            if (Savelist["Step_number"] != -1) and (Savelist["Step_Des"] == "") and (Savelist["image_name2"] != None) and (upload_images != None):
                flash(f"Please add Step Description!", 'error')
    else:
        flash(f"Please create the recipe first!", 'error')
        return redirect(url_for('recipes.create_recipe'))

    Submit = request.form.get('Submit')
    if Submit != None:
        recipe_id = Savelist["RecipeId"]
        #fetch steps from db
        Steps = ""
        obj = Recipestep.query.filter_by(recipe_id = recipe_id).all()

        step_list = []
        image_list = []
        for o in obj:
            Steps = f"Step.{o.step_no} --> {o.step_comment}  \n"
            step_list.append(Steps)
            image_temp = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': o.photo})
            image_list.append(image_temp)
        length1 = len(step_list)
        while length1 < 4:
            step_list.append(f"Step.{length1}  \n")
            image_list.append(None)
            length1 += 1
        
        recipe_data = Recipes.query.filter_by(id = recipe_id).first()
        
        IngredientList.clear()#reset
        #clean global list
        initial()
        return redirect(url_for('recipes.view_recipe',recipeName = recipe_data.name,recipeId = recipe_data.id ))

    Step_No = None
    Step_Number = 0
    if Savelist["RecipeId"]:
        Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
    
    if Step_No != None:
        if Step_No[0] != None:
            Step_Number = Step_No[0]
        else:
            Step_Number = 0
    else:
        Step_Number = 0

    
    return render_template("add_discription.html", user=current_user, current_step = current_step, Step_Number = (Step_Number+1), color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"], des_step = Shown_discription)


    
@recipes.route('/Add ingredient', methods=['GET', 'POST'])
def Add_ingredient():
    if check_create(Savelist["RecipeName"],current_user.id) is False:
        flash(f"Please create the recipe first!", 'error')
        return redirect(url_for('recipes.create_recipe'))
    IngredientList = []
    IngredientList.clear()
    Ingredients = Ingredient.query.filter_by(recipe_id=Savelist["RecipeId"]).order_by(Ingredient.id.asc()).all()
    for ingre in Ingredients:
        Dict = dict({'Dosage' : ingre.dosage, 'UnitName' : ingre.unit_name, 'Ingredient' : ingre.ingredient})
        IngredientList.append(Dict) 
            
        
    Contents = take_ingredientList_into_str(IngredientList)
    
    Ingredients = get_ingre_in_order()
    return render_template("add_ingradient.html", user=current_user, IngreContents = Contents, color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"], ingredients =  Ingredients)
    
   
@recipes.route('/upload image', methods=['GET', 'POST'])
def upload_image():
    
    if check_create(Savelist["RecipeName"],current_user.id) is True:    #is true, already created recipe
        button3 = request.form.get('button3')
        if button3 != None:
            file1 = request.files['file1']

            # if user does not select file, browser also
            # submit an empty part without filename
            if file1 != None:
                file_data = file1
                
                if file1.filename == '':
                    flash('Continue to create recipe')
                    return redirect(request.url)
                if file1 and allowed_file(file1.filename):
                    filename = secure_filename(file1.filename)
                    recipe_data = Recipes.query.filter_by(id=Savelist["RecipeId"]).first()
                    recipe_data.photo = filename

                    file1.save(filename)
                    s3.upload_file(
                        Bucket = 'comp3900-w18b-sheeesh',
                        Filename=filename,
                        Key = filename
                    )
                    os.remove(filename)
                    image_datas1_read = file_data.read()
                    image1 = base64.b64encode(image_datas1_read).decode('ascii')
                    db.session.commit()

                    image_datas1 = image1
                    Savelist["image_name1"] = filename
                        
                    if recipe_data.photo != None:
                        flash(f"Recipe photo upload Successfully!")
                    Savelist["color_2"] = "red"
                    return redirect(url_for('recipes.Add_ingredient'))
    else:
        
        flash(f"Please create the recipe first!", 'error')
        return redirect(url_for('recipes.create_recipe'))
        
    recipename = ""
    if Savelist["RecipeName"] != None:
        recipename = Savelist["RecipeName"]
    return render_template("upload_image.html", user=current_user, recipename = recipename, color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"])

@recipes.route('/Create recipe', methods=['GET', 'POST'])
def create_recipe():
    
    Savelist["Is_creating"] = True
    
    IngredientList.clear()

    if request.method == 'POST':
        RecipeName = request.form.get('Recipe Name')
        Description = request.form.get('Recipe Des')
        Serving = request.form.get('Servings')
        Meal_type = request.form.get('Meal type')
        Baking = request.form.get('Baking')
        Frying = request.form.get('Frying')
        Grilling = request.form.get('Grilling')
        Steaming = request.form.get('Steaming')
        Braising = request.form.get('Braising')
        Stewing = request.form.get('Stewing')

        if RecipeName and Description and (Serving != '0') and Meal_type:  #check not empty, create recipe
            create_recipe(RecipeName,Description,Serving,Meal_type)
            Savelist["RecipeName"] = RecipeName
            if Baking:
                Baking = Method(recipe_id = Savelist["RecipeId"], method=Baking)
                db.session.add(Baking)
                db.session.commit()    
            if Frying:
                Frying = Method(recipe_id = Savelist["RecipeId"], method=Frying)
                db.session.add(Frying)
                db.session.commit() 
            if Grilling:
                Grilling = Method(recipe_id = Savelist["RecipeId"], method=Grilling)
                db.session.add(Grilling)
                db.session.commit() 
            if Steaming:
                Steaming = Method(recipe_id = Savelist["RecipeId"], method=Steaming)
                db.session.add(Steaming)
                db.session.commit()
            if Braising:
                Braising = Method(recipe_id = Savelist["RecipeId"], method=Braising)
                db.session.add(Braising)
                db.session.commit()
            if Stewing:
                Stewing = Method(recipe_id = Savelist["RecipeId"], method=Stewing)
                db.session.add(Stewing)
                db.session.commit()
             
            #methods = Method.query.filter_by(recipe_id=Savelist["RecipeId"]).first()

            flash(f"Create Recipe {RecipeName} Successfully!")
            # change the color on page to show complete this part
            Savelist["color_1"] = "red"
            return redirect(url_for('recipes.upload_image'))

        if (RecipeName == ''):
            flash("Please enter recipe name", 'error')
        if (Description == ''):
            flash("Please add disription", 'error')
        if (Serving == '0'):
            flash("Serving can't be 0", 'error')
        if(Meal_type == ''):
            flash("Please choose a meal_type", 'error')
        
        
    return render_template("create_recipe.html", user=current_user, color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"])

@recipes.route('/edit recipe', methods = ['GET', 'POST'])
def edit_recipe():
    recipe_id = Savelist["RecipeId"]
    recipe = Recipes.query.filter_by(id=recipe_id).first()
        
    #find recipe success
    if recipe.creates != current_user.id:
        flash("You are not the owner of this recipe", 'error')
        return redirect(url_for('recipes.view_recipe',recipeName = recipe.name,recipeId = recipe.id ))

    Savelist["contents"] = generate_ingreStr_by_recipeId(Savelist["RecipeId"])

    if request.method == 'POST':
        RecipeName = request.form.get('Recipe Name')
        Description = request.form.get('Recipe Des')
        Serving = request.form.get('Servings')
        Meal_type = request.form.get('Meal type')
        Baking = request.form.get('Baking')
        Frying = request.form.get('Frying')
        Grilling = request.form.get('Grilling')
        Steaming = request.form.get('Steaming')
        Braising = request.form.get('Braising')
        Stewing = request.form.get('Stewing')

        button_create = request.form.get('create')
        if button_create != None:
            if (Serving == '0'):
                flash("Serving can't be 0", 'error')
                return redirect(url_for('recipes.edit_recipe'))
            if Meal_type:
                recipe.meal_type = Meal_type
                db.session.commit()
                flash(f"Meal type updated Successfully!")
            if RecipeName:
                recipe.name = RecipeName
                db.session.commit()
                flash(f"Recipe name updated Successfully!")
            if Description:
                recipe.description = Description
                flash(f"Description updated Successfully!")
                db.session.commit()
            if Serving and (Serving != 0):
                recipe.serving = Serving
                db.session.commit()
                flash(f"Serving updated Successfully!")
            if Baking or Frying or Grilling or Steaming or Braising:
                methods = Method.query.filter_by(recipe_id=recipe_id).all()
                for i in methods:
                    if i.recipe_id == recipe_id:
                        db.session.delete(i)
                db.session.commit()
                if Baking:
                    Baking = Method(recipe_id = Savelist["RecipeId"], method=Baking)
                    db.session.add(Baking)
                    db.session.commit()    
                if Frying:
                    Frying = Method(recipe_id = Savelist["RecipeId"], method=Frying)
                    db.session.add(Frying)
                    db.session.commit() 
                if Grilling:
                    Grilling = Method(recipe_id = Savelist["RecipeId"], method=Grilling)
                    db.session.add(Grilling)
                    db.session.commit() 
                if Steaming:
                    Steaming = Method(recipe_id = Savelist["RecipeId"], method=Steaming)
                    db.session.add(Steaming)
                    db.session.commit()
                if Braising:
                    Braising = Method(recipe_id = Savelist["RecipeId"], method=Braising)
                    db.session.add(Braising)
                    db.session.commit()
                if Stewing:
                    Stewing = Method(recipe_id = Savelist["RecipeId"], method=Stewing)
                    db.session.add(Stewing)
                    db.session.commit()
                flash(f"Update Method Successfully!")
            flash(f"Update Recipe {RecipeName} Successfully!")
            # change the color on page to show complete this part
            Savelist["color_1"] = "red"
            return redirect(url_for('recipes.edit_photo'))
    return render_template("edit_recipe.html", user=current_user, recipe = recipe, color1 = Savelist["color_1"],
        color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"])

@recipes.route('/edit recipe image', methods = ['GET', 'POST'])
def edit_photo():
    #is true, already created recipe
    button3 = request.form.get('button3')
    if button3 != None:
        file1 = request.files['file1']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file1 != None:
            file_data = file1
            
            if file1.filename == '':
                flash('Continue to create recipe')
                return redirect(request.url)
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                recipe_data = Recipes.query.filter_by(id=Savelist["RecipeId"]).first()
                recipe_data.photo = filename

                file1.save(filename)
                s3.upload_file(
                    Bucket = 'comp3900-w18b-sheeesh',
                    Filename=filename,
                    Key = filename
                )
                image_datas1_read = file_data.read()
                image1 = base64.b64encode(image_datas1_read).decode('ascii')
                db.session.commit()

                image_datas1 = image1
                Savelist["image_name1"] = filename
                    
                if recipe_data.photo != None:
                    flash(f"Recipe photo updated Successfully!")
                Savelist["color_2"] = "red"
                return redirect(url_for('recipes.edit_ingredient'))
        
    recipename = ""
    if Savelist["RecipeName"] != None:
        recipename = Savelist["RecipeName"]
    return render_template("edit_recipe_image.html", user=current_user, recipename = recipename, color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"])

@recipes.route('/delete ingredient', methods = ['POST', 'GET'])
def delete_ingredient():
    if request.method == 'POST':
        ingredient = json.loads(request.data)

        ingredient_id = ingredient['ingredient_id']
        ingredient_delete = Ingredient.query.filter_by(id = ingredient_id).first()

        db.session.delete(ingredient_delete)
        db.session.commit()
        
        IngredientList.clear()
        Ingredients = Ingredient.query.filter_by(recipe_id=Savelist["RecipeId"]).order_by(Ingredient.id.asc()).all()
        for ingre in Ingredients:
            Dict = dict({'Dosage' : ingre.dosage, 'UnitName' : ingre.unit_name, 'Ingredient' : ingre.ingredient})
            IngredientList.append(Dict) 
        flash('Deleted ingredient successfully!', category='success')
        if Savelist["Is_creating"] == False:
            return redirect(url_for('recipes.edit_ingredient'))
        return redirect(url_for('recipes.Add_ingredient'))

@recipes.route('/modify ingredient', methods = ['POST', 'GET'])
def modify_ingredient():
    if request.method == 'POST':
        Contents = Savelist["contents"]
        
        ingredient = json.loads(request.data)
        

        ingredient_id = ingredient['ingredient_id']
        Dosage = ingredient['Dosage']
        UnitName = ingredient['UnitName']
        MyIngredient = ingredient['MyIngredient']
        
        ingredient_edit = Ingredient.query.filter_by(id = ingredient_id).first()

        if Dosage:
            ingredient_edit.dosage = Dosage
        if UnitName:
            ingredient_edit.unit_name = UnitName
        if MyIngredient:
            ingredient_edit.ingredient = MyIngredient
        db.session.commit()
        Savelist["contents"] = Contents
        Savelist["color_3"] = "red"
        IngredientList.clear()
        Ingredients = Ingredient.query.filter_by(recipe_id=Savelist["RecipeId"]).order_by(Ingredient.id.asc()).all()
        for ingre in Ingredients:
            Dict = dict({'Dosage' : ingre.dosage, 'UnitName' : ingre.unit_name, 'Ingredient' : ingre.ingredient})
            IngredientList.append(Dict) 
        flash(f"Update ingredient {MyIngredient} successfully!")
        if Savelist["Is_creating"] == False:
            return redirect(url_for('recipes.edit_ingredient'))
        return redirect(url_for('recipes.Add_ingredient'))

#Add ingrdient
@recipes.route('/push ingredient', methods = ['POST', 'GET'])
def push_ingredient():
    if request.method == 'POST':
        Contents = Savelist["contents"]
        ingredient = json.loads(request.data)
        
        Dosage = ingredient['Dosage']
        UnitName = ingredient['UnitName']
        Ingredient_name = ingredient['MyIngredient']

        if Dosage and UnitName and Ingredient_name:
            #edit ingredient
            #we can begin to add ingredients
            
            Savelist["contents"] = Contents
            Savelist["color_3"] = "red"
            new_ingredient = Ingredient(recipe_id = Savelist["RecipeId"], dosage = Dosage, unit_name = UnitName,
            ingredient = Ingredient_name)
            db.session.add(new_ingredient)
            db.session.commit()

            # Update IngredientList
            IngredientList.clear()
            Ingredients = Ingredient.query.filter_by(recipe_id=Savelist["RecipeId"]).order_by(Ingredient.id.asc()).all()
            for ingre in Ingredients:
                Dict = dict({'Dosage' : ingre.dosage, 'UnitName' : ingre.unit_name, 'Ingredient' : ingre.ingredient})
                IngredientList.append(Dict)
            if Savelist["Is_creating"] == False:
                return redirect(url_for('recipes.edit_ingredient'))
            return redirect(url_for('recipes.Add_ingredient'))
    
#Add ingrdient
@recipes.route('/edit ingredient', methods = ['POST', 'GET'])
def edit_ingredient():
    # Update IngredientList
    IngredientList = []
    IngredientList.clear()
    Ingredients = Ingredient.query.filter_by(recipe_id=Savelist["RecipeId"]).order_by(Ingredient.id.asc()).all()
    for ingre in Ingredients:
        Dict = dict({'Dosage' : ingre.dosage, 'UnitName' : ingre.unit_name, 'Ingredient' : ingre.ingredient})
        IngredientList.append(Dict) 
            
        
    Contents = take_ingredientList_into_str(IngredientList)
    Ingredients = get_ingre_in_order()
    return render_template("edit_ingredient.html", user=current_user, IngreContents = Contents, color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"], ingredients =  Ingredients)

@recipes.route('/delete discription', methods = ['GET', 'POST'])
def delete_discription():
    if request.method == 'POST':
        step = json.loads(request.data)
        recipe_id = step['id']
        step_no = step['step_no']
        count_number = Recipestep.query.filter_by(recipe_id = recipe_id).all()
        if len(count_number) <= 1:
            flash("At least contain one step discription", 'error')
            Savelist["can't_be_zero"] = True
            if Savelist["Is_creating"] == True:
                return redirect(url_for('recipes.add_discription'))
            return redirect(url_for('recipes.edit_discription'))
        else:
            step_delete = Recipestep.query.filter_by(recipe_id = recipe_id, step_no = step_no).first()

            db.session.delete(step_delete)
            db.session.commit()

            if Savelist["Is_creating"] == True:
                return redirect(url_for('recipes.add_discription'))
            return redirect(url_for('recipes.edit_discription'))

@recipes.route('/edit discription', methods = ['GET', 'POST'])
def edit_discription():
    if Savelist["can't_be_zero"] == True:
        flash("At least contain one step discription", 'error')
        Savelist["can't_be_zero"] = False

    StepNo = request.form.get('step_number')
    StepDes = request.form.get('discriptions')
    
    current_step = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).first()
    Find = request.form.get('find')
    obj = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).all()
    # We assume there is at last one discription
    Shown_discription = ""
    if obj != []:
        Shown_discription = obj[0]
    if Find != None:
        Find_discription = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"], step_no = StepNo).first()
        if Find_discription == None:
            if Savelist["deleting_step"] == True:
                flash("successfully deleting current step")
            else:
                flash("Don't create this step yet", 'error')
            Savelist["deleting_step"] = False
        else:
            Shown_discription = Find_discription


    upload_images = request.form.get('upload_images')
    if upload_images != None:
        file2 = request.files['file2']
        if file2 != None:
            file_data = file2

            if file2.filename == '':
                flash('Continue to create recipe')
                return redirect(request.url)
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
            

                file2.save(filename)
                s3.upload_file(
                    Bucket = 'comp3900-w18b-sheeesh',
                    Filename=filename,
                    Key = filename
                )
                image_datas2_read = file_data.read()
                image2 = base64.b64encode(image_datas2_read).decode('ascii')
                image_datas2 = image2
                Savelist["image_name2"] = filename

                Savelist["Step_number"] = StepNo
                Savelist["Step_Des"] = StepDes
        no_list = []
        obj = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).all()
        for o in obj:
            no_list.append(int(o.step_no))
            if int(Savelist["Step_number"]) == int(o.step_no):
                if StepNo:
                    o.step_no = StepNo
                if StepDes:
                    o.step_comment = StepDes
                if Savelist["image_name2"]:
                    o.photo = Savelist["image_name2"]
                db.session.commit()

                # Set to current step
                Shown_discription = o

        
        if int(Savelist["Step_number"]) not in no_list:
            if StepNo and StepDes and Savelist["image_name2"]:
                # we can begin to add steps                
                #get the latest id of this recipeName
                recipe_id = Savelist["RecipeId"]
                new_step = Recipestep(recipe_id = recipe_id, step_no = StepNo, step_comment = StepDes, photo = Savelist["image_name2"])
                db.session.add(new_step)
                db.session.commit()             # Commits changes
                # Set to current step
                Shown_discription = new_step
                flash(f"Added comment and photo at Step.{StepNo}!")
        else:
            if Savelist["can't_be_zero"] == True:
                flash("At least contain one step discription", 'error')
                Savelist["can't_be_zero"] = False
            elif Savelist["deleting_step"] == True:
                flash("successfully deleting current step")
                Savelist["deleting_step"] = False
            else:    
                flash(f"Update comment and photo at Step.{StepNo}!")
    
        Savelist["color_4"] = "red"

    Submit = request.form.get('Submit')
    if Submit != None:
        recipe_id = Savelist["RecipeId"]
        #fetch steps from db
        Steps = ""
        obj = Recipestep.query.filter_by(recipe_id = recipe_id).all()

        step_list = []
        image_list = []
        for o in obj:
            Steps = f"Step.{o.step_no} --> {o.step_comment}  \n"
            step_list.append(Steps)
            image_temp = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': o.photo})
            image_list.append(image_temp)
        length1 = len(step_list)
        while length1 < 4:
            step_list.append(f"Step.{length1}  \n")
            image_list.append(None)
            length1 += 1

        recipe_data = Recipes.query.filter_by(id = recipe_id).first()
        
        image1 = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': recipe_data.photo})
        
        
        IngredientList.clear()#reset
        
        #clean global list
        initial()
        return redirect(url_for('recipes.view_recipe',recipeName = recipe_data.name,recipeId = recipe_data.id ))

    Step_No = None
    Step_Number = 0
    if Savelist["RecipeId"]:
        Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
    
    if Step_No != None:
        if Step_No[0] != None:
            Step_Number = Step_No[0]
        else:
            Step_Number = 0
    else:
        Step_Number = 0

    
    return render_template("edit_discription.html", user=current_user, current_step = current_step, Step_Number = (Step_Number+1), color1 = Savelist["color_1"],
            color2 = Savelist["color_2"], color3 = Savelist["color_3"], color4 = Savelist["color_4"], des_step = Shown_discription)



@recipes.route('/<recipeName>.<int:recipeId>', methods=['GET', 'POST'])
def view_recipe(recipeName, recipeId):
    #for cookbook
    cookbook_my = Cookbooks.query.filter_by(contains = current_user.id).all()
    #add into cookbook
    book_add = request.form.get('cookbook')
    
    if book_add is not None:
        new_recipe_inbook = Cookbooks_lists(cookbook_id = book_add, recipe_id = recipeId)
        db.session.add(new_recipe_inbook)
        db.session.commit()
        flash('Added into CookBook!', category='success')

    
    IngredientList.clear()
    Ingredients = Ingredient.query.filter_by(recipe_id=recipeId).all()
    for ingre in Ingredients:
        Dict = dict({'Dosage' : ingre.dosage, 'UnitName' : ingre.unit_name, 'Ingredient' : ingre.ingredient})
        IngredientList.append(Dict)
    Savelist["edit_ingredient"] = False
    recipe = Recipes.query.filter_by(id=recipeId).first()
    
    if Savelist["already_delete"] == True:
        flash("Delete successfully")
        Savelist["already_delete"] = False
        return redirect(url_for('views.home'))
    if recipe is None and Savelist["already_delete"] == False:
        flash("No recipe exists with this name and id.", category="error")
        return redirect(url_for('views.home'))

    #find recipe success
    RecipeImage = None
    Contents = generate_ingreStr_by_recipeId(recipe.id)
    if recipe.photo != None:
        RecipeImage = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': recipe.photo})
    
    #fetch steps from db
    Steps = ""
    obj = Recipestep.query.filter_by(recipe_id = recipe.id).all()

    step_list = []
    image_list = []
    for o in obj:
        Steps = f"Step.{o.step_no} --> {o.step_comment}  \n"
        step_list.append(Steps)
        image_temp = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': o.photo})
        image_list.append(image_temp)
    length1 = len(step_list)
    while length1 < 4:
        step_list.append(f"Step.{length1}  \n")
        image_list.append(None)
        length1 += 1
    Savelist["RecipeId"] = recipe.id
    obj = Recipestep.query.filter_by(recipe_id = recipe.id).all()
    comments = retrieve_comments(recipe.id) # Get comments for recipe and user information
    rating = get_rating(recipe.num_of_likes, recipe.num_of_dislikes)
    
    methods = Method.query.filter_by(recipe_id=Savelist["RecipeId"]).all()
    if current_user.is_authenticated:
        if not StarredRecipes.query.filter_by(recipe_id=recipe.id, contains=current_user.id).first():
            star_status = "unstarred"
        else:
            star_status = "starred"
    else:
        star_status = "unstarred"


    #Create recipe view history
    if current_user.is_authenticated:
        exist_history = History.query.filter_by(userid = current_user.id, recipe = recipeId).first()
        if exist_history != None:
            date = datetime.date(datetime.now())
            time = datetime.time(datetime.now())
            exist_history.last_view_time = time
            exist_history.last_view_date = date
            db.session.commit()
        else:
            history = History(userid = current_user.id, recipe = recipe.id)
            db.session.add(history)
            db.session.commit()
    
    
    
    conn = psycopg2.connect(
    database="rec", user='postgres', password='aa', host='localhost', port= '5432'
)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # finds similar recipes to the one currently being looked at
    # works similarly to history similar recipes
    # i1 is a list of ingredients except for the current recipe
    # i2 is a list of ingredients from the current recipe
    # join those two to get t1 to find the list of recipes that have the same ingredients
    # then similarly done to j1 and j2 but in the opposite way for the ingredients to find any missing cases (explained above in history)
    # then that is unioned to t1 to get t2 
    # then join that list to recipes to get the name and photo and count how many similarities, then order from highest to lowest
    
    
    sql ='''select t2.rec_id, count(*), name, photo
            from
            (select * from
                (select * from
                    (select id, recipe_id as rec_id, ingredient from Ingredient where recipe_id != %s) i1
                    inner join
                    (select id, recipe_id, ingredient from Ingredient where recipe_id = %s) i2
                    on lower(concat('%%', i2.ingredient, '%%')) LIKE lower(concat('%%', i1.ingredient, '%%'))) as t1
                union
                (select * from
                    (select id, recipe_id as rec_id, ingredient from Ingredient where recipe_id != %s) j1
                    inner join
                (select id, recipe_id, ingredient from Ingredient where recipe_id = %s) j2
                on lower(concat('%%', j1.ingredient, '%%')) LIKE lower(concat('%%', j2.ingredient, '%%')))) as t2
            join
                recipes r on (r.id = t2.rec_id)
            group by t2.rec_id, r.name, r.photo
            order by count desc
            limit 7;'''
    
    
    id = str(recipe.id)
    
    cursor.execute(sql, (id, id, id, id))
    res=cursor.fetchall()
    
    
    
    #sqlalchemy attemps
    
    #sub = Ingredient.query.filter_by(recipe_id = recipe.id).with_entities(Ingredient.recipe_id, func.count(Ingredient.recipe_id)).order_by(Ingredient.recipe_id).group_by(Ingredient.recipe_id).all()
    # ing = Ingredient.query.filter(Ingredient.recipe_id != recipe.id).with_entities(Ingredient.ingredient).subquery()
    # print(ing)
    
    # qry = Ingredient.query.outerjoin(ing, Ingredient.ingredient==ing)
    # print(qry)
    # sub = Ingredient.query.filter_by(recipe_id=recipe.id).all()
    # q = ing.union(sub)
    
    # print(q)
    # que = Ingredient.query.filter_by(recipe_id = recipe.id).outerjoin(sub).all()
    # print(que)
    #res = sub.query(func.count(sub.recipe_id)).scalar()
    #print(res)
    # res = Ingredient.query.filter(Ingredient.ingredient.in_(sub)).all()
    # for res in res:
    #     print(res)
    
    #to tell which image should use for user
    if len(get_user_image(recipeId)) == 24:
        UserImage = get_default_user_img()
    else:
        UserImage = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': get_user_image(recipeId)})
    
    # Link the creator's name as url
    creator_name = recipe.creator.split(" ")
    profile = Profiles.query.filter_by(owns = recipe.creates, last_name = creator_name[1], first_name = creator_name[0]).first()
    
    return render_template("recipe.html", user=current_user, RecipeName=recipe.name, Descriptions=recipe.description,MyIngredient = Contents,
        recipe_id = recipe.id,image1 = RecipeImage, query = obj, comments=comments, creates = recipe.creates, recipe=recipe, type="recent", 
            meal_type = recipe.meal_type, methods=methods, star_status=star_status, res=res, UserImage = UserImage, UserName = recipe.creator, 
            rating=rating, cookbook_my = cookbook_my, profile = profile)
        
         



@recipes.route('/Delete recipe', methods=['GET', 'POST'])
def delete_recipe():
    #delete the recipe using recipeId
    recipe_id = Savelist["RecipeId"]

    recipe = Recipes.query.filter_by(id=recipe_id).first()
        
    #find recipe success
    if recipe != None:
        if recipe.creates != current_user.id:
            flash("You are not the owner of this recipe", 'error')
            return redirect(url_for('recipes.view_recipe',recipeName = recipe.name,recipeId = recipe.id ))

    # Delete associated likes about recipe
    likes = Likes.query.filter_by(has=recipe_id).all()
    for like in likes:
        db.session.delete(like)


    # Delete associated comments about recipe
    comments = Comments.query.filter_by(has=recipe_id).all()
    for comment in comments:
        db.session.delete(comment)


    # Delete associated likes
    likes = Likes.query.filter_by(own=current_user.id).all()
    for like in likes:
        db.session.delete(like)


    # Delete associated comments
    comments = Comments.query.filter_by(owns=current_user.id).all()
    for comment in comments:
        db.session.delete(comment)

    #delete ingredient
    ingre = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    if ingre != None:
        for i in ingre:
            if i.recipe_id == recipe_id:
                db.session.delete(i)

    #delete steps
    steps = Recipestep.query.filter_by(recipe_id=recipe_id).all()
    if steps != None:
        for s in steps:
            if s.recipe_id == recipe_id:
                db.session.delete(s)

    #delete history
    historys = History.query.filter_by(recipe=recipe_id).all()
    if historys != None:
        for s in historys:
            if s.recipe == recipe_id:
                db.session.delete(s)

    #delete Method
    methods = Method.query.filter_by(recipe_id=recipe_id).all()
    if methods != None:
        for s in methods:
            if s.recipe_id == recipe_id:
                db.session.delete(s)

    #delete recipe
    recipe = Recipes.query.filter_by(id=recipe_id).first()
    if recipe != None:
        db.session.delete(recipe)
        db.session.commit()
    flash("Delete successfully")
    Savelist["already_delete"] = True
    return redirect(url_for('views.home'))

# return a view of a random recipe
@recipes.route('/recipe/random')
def random_recipe():
    rand_num = random.randrange(0, db.session.query(Recipes).count())
    rand_recipe = db.session.query(Recipes)[rand_num]
    name = rand_recipe.name
    id = rand_recipe.id
    return view_recipe(name, id) 

# star and unstar a recipe
@recipes.route('/recipe/star', methods=['GET', 'POST'])
def star_recipe():
    message = ''
    if request.method == "POST":
        star_status = request.form['status']
        user_id = request.form['user']
        recipe_id = request.form['recipe']

        # sub_status = "subscribe" or "subscribed" with the quotations included. Later add an alert for unsubscribing and make sure only s
        # logged in users can subscribe. Can't subscribe to yourself (maybe add this).

    if str(star_status) == '"starred"':
        new_star = StarredRecipes(recipe_id=recipe_id, contains=user_id) # user's subscribed to list
        db.session.add(new_star)
        
        message = "user " + str(user_id) + " has starred recipe " + str(recipe_id)
    # code for unsubscribing
    elif str(star_status) == '"unstarred"':
        del_star = StarredRecipes.query.filter_by(recipe_id=recipe_id, contains=user_id).first()
  
        db.session.delete(del_star)
        message = "user " + str(user_id) + " has unstarred recipe " + str(recipe_id)

    db.session.commit()

    
    return message

# View user's starred recipes
@recipes.route('recipes/starred', methods=['GET', 'POST'])
def view_starred():
    query = StarredRecipes.query.filter_by(contains=current_user.id).all()
    recipes = []
    profiles = []
    for item in query:

        recipe = Recipes.query.filter_by(id=item.recipe_id).first()
        profile = Profiles.query.filter_by(profile_id=recipe.creates).first()
        setattr(recipe, "custom_url", profile.custom_url)
        recipes.append(recipe)
    type = '#'
    if StarredRecipes.query.filter_by(contains=current_user.id).count() == 0:
        type = 'empty'

    return render_template("starred.html", user=current_user, query=recipes, type=type)


#############helper funcs##########
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def create_recipe (RecipeName, Description, Serving, Meal_type):
    #add name and description to db
    user = Profiles.query.filter_by(owns = current_user.id).first()

    new_recipe = Recipes(name = RecipeName, description = Description, 
        serving = Serving, creates = current_user.id, creator = (user.first_name+" "+user.last_name), meal_type=Meal_type)

    
    db.session.add(new_recipe)
    db.session.commit()             # Commits changes

    Savelist["RecipeId"] = new_recipe.id

#def add_step (recipe_id, step_no, )
    

#add ingredients to IngredientList
def add_ingredients_to_list(Dosage,UnitName,MyIngredient):
    #put in a dictionary temporary, after the recipe create add the recipe id
    Dict = dict({'Dosage' : Dosage, 'UnitName' : UnitName, 'Ingredient' : MyIngredient})
    IngredientList.append(Dict)


def add_ingredient_to_db(recipe_id):
    step = 0
    for item in IngredientList:
        Dosage = item.get('Dosage')
        UnitName = item.get('UnitName')
        MyIngredient = item.get('Ingredient')
        
        new_ingredient = Ingredient(recipe_id = recipe_id, dosage = Dosage, unit_name = UnitName,
            ingredient = MyIngredient)
        db.session.add(new_ingredient)
        db.session.commit()             # Commits changes
        
        step += 1

def take_ingredientList_into_str(IngredientLists):
    Contents = ""
    counter = 1
    for item in IngredientLists:
        Dosage = item.get('Dosage')
        UnitName = item.get('UnitName')
        MyIngredient = item.get('Ingredient')
        Contents += (f"{counter}) --> {Dosage} {UnitName} {MyIngredient}.     "
                    f"\n")
        counter += 1
    return Contents

def check_create(RecipeName,userid):

    obj = Recipes.query.filter_by(name= RecipeName, id = Savelist["RecipeId"]).first()
    if obj != None:
        return True
    return False

#find all ingredient relate to recipeId in db, generate a Str
def generate_ingreStr_by_recipeId(recipeId):
    Contents = ""
    counter = 1
    ingre = Ingredient.query.filter_by(recipe_id=recipeId).all()
    for item in ingre:
        Dosage = item.dosage
        UnitName = item.unit_name
        MyIngredient = item.ingredient
        Contents += (f"{counter}. --> {Dosage} {UnitName} {MyIngredient}.     "
                    f" ")
        counter += 1
    return Contents

def initial():
    Savelist["Serving"] = None
    Savelist["RecipeName"] = None
    Savelist["RecipeId"] = None
    Savelist["Dosage"] = None
    Savelist["UnitName"] = None
    Savelist["MyIngredient"] = None
    Savelist["Description"] = None
    Savelist["image_datas1"] = None
    Savelist["image_datas2"] = None
    Savelist["Step_number"] = -1   #step number can't be None
    Savelist["Step_Des"] = None
    Savelist["image_name2"] = None
    Savelist["image_name1"] = None
    Savelist["contents"] = ''
    Savelist["color_1"] = ''
    Savelist["color_2"] = ''
    Savelist["color_3"] = ''
    Savelist["color_4"] = ''
    Savelist["Is_creating"] = False
#find user image by userId
def get_user_image(recipeId):
    recipe = Recipes.query.filter_by(id = recipeId).first()
    user = Profiles.query.filter_by(owns = recipe.creates).first()
    return user.profile_pic

def get_default_user_img():
    image_file = url_for('static', filename='default_user.jpg')
    return image_file

# For geting ingredient order
def get_ingre_in_order():
    Ingredients = Ingredient.query.filter_by(recipe_id=Savelist["RecipeId"]).order_by(Ingredient.id.asc()).all()
    order = 0
    lst = []
    for i in Ingredients:
        ingre_order = ingre(i, order)
        lst.append(ingre_order)
        order += 1
    return lst