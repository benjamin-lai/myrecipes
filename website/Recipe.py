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
from .models import Users, Recipes, Ingredient, Contents, Recipestep, Profiles, Method, History
from .review import create_comment, retrieve_comments
from . import db
from sqlalchemy import desc
from sqlalchemy import func
import base64
import boto3
from datetime import datetime

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


@recipes.route('/Trending Section', methods = ['GET','POST'])
def trending_section():
    recipes = Recipes.query.order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "All types")

@recipes.route('/Trending Section.Starter', methods = ['GET','POST'])
def trending_section_Starter():
    print("Starter")
    recipes = Recipes.query.filter_by(meal_type = "Starter").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Starter")
    
@recipes.route('/Trending Section.Main', methods = ['GET','POST'])
def trending_section_Main():
    print("Main")
    recipes = Recipes.query.filter_by(meal_type = "Main").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Main")

@recipes.route('/Trending Section.Dessert', methods = ['GET','POST'])
def trending_section_Dessert():
    print("Dessert")
    recipes = Recipes.query.filter_by(meal_type = "Dessert").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Dessert")

@recipes.route('/Trending Section.Snack', methods = ['GET','POST'])
def trending_section_Snack():
    print("Snack")
    recipes = Recipes.query.filter_by(meal_type = "Snack").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Snack")

@recipes.route('/Trending Section.Breakfast', methods = ['GET','POST'])
def trending_section_Breakfastk():
    print("Breakfast")
    recipes = Recipes.query.filter_by(meal_type = "Breakfast").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Breakfastk")

@recipes.route('/Trending Section.Drink', methods = ['GET','POST'])
def trending_section_Drink():
    print("Drink")
    recipes = Recipes.query.filter_by(meal_type = "Drink").order_by((Recipes.num_of_likes - Recipes.num_of_dislikes).desc()).all()
    trending = []
    for i in recipes:
        if i.num_of_likes > i.num_of_dislikes:
            trending.append(i)
    return render_template("trending_section.html", query=trending, type="recent", meal_type = "Drink")

@recipes.route('/history', methods = ['GET','POST'])
def history():
    histories = History.query.filter_by(userid = current_user.id).order_by(History.last_view_time.desc()).all()
    query = []
    for i in histories:
        recipes = Recipes.query.filter_by(id = i.recipe).all()
        for j in recipes:
            query.append(j)
    return render_template("history.html", query=query, type="recent")

@recipes.route('/history.<int:recipeId>', methods=['GET', 'POST'])
def delete_history(recipeId):
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
    #return render_template("history.html", query=query, type="recent")

@recipes.route('/Recipe cards', methods = ['GET','POST'])
def recipe_cards():
    query = Recipes.query.order_by(Recipes.id.desc()).all()
    return render_template("Recipe_card.html", query=query, type="recent")

@recipes.route('/recipes', methods = ['GET','POST'])
def recipe():
    recipe_id = request.form.get('recipe_id')
    #print(f"recipe id is  {recipe_id}")
    #print(Savelist["RecipeId"])
    print(Savelist["RecipeId"])
    print("recipe below")
    recipe_data = Recipes.query.filter_by(id = 38).first()
    print(recipe_data.photo)
    print(recipe_data.name)
    image1 = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': recipe_data.photo})
    print(image1)
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
        return render_template("recipe.html", user=current_user, name=recipe_data.name, Descriptions=recipe_data.description, image1 = image1)


@recipes.route('/Create recipe', methods=['GET', 'POST'])
def create_recipe():
    #Contents = take_ingredientList_into_str()
    Contents = ""
    ##IngredientList.clear()#reset
    
    print("reset1")
    print(IngredientList)
    #image_datas1 = None
    #image_datas2 = None
    if request.method == 'POST':
        RecipeName = request.form.get('Recipe Name')
        Description = request.form.get('Recipe Des')
        Serving = request.form.get('Servings')
        Dosage = request.form.get('dosage')
        UnitName = request.form.get('Unit Name')
        MyIngredient = request.form.get('Ingredient Name')
        StepNo = request.form.get('step_number')
        StepDes = request.form.get('discriptions')
        Meal_type = request.form.get('Meal type')
        Baking = request.form.get('Baking')
        Frying = request.form.get('Frying')
        Grilling = request.form.get('Grilling')
        Steaming = request.form.get('Steaming')
        Braising = request.form.get('Braising')
        Stewing = request.form.get('Stewing')

        if RecipeName and Description and Serving and Meal_type:  #check not empty, create recipe
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
             
            methods = Method.query.filter_by(recipe_id=Savelist["RecipeId"]).first()
            

            flash(f"Create Recipe {RecipeName} Successfully!")

        if check_create(Savelist["RecipeName"],current_user.id) is True:    #is true, already created recipe
            print(f"{Dosage} + {UnitName} + {MyIngredient}")
            button3 = request.form.get('button3')
            if button3 != None:
                file1 = request.files['file1']
        
                # if user does not select file, browser also
                # submit an empty part without filename
                if file1 != None:
                    file_data = file1
                    #Savelist["image_datas1"] = file_data
                    #image_datas1=file_data.read()
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
                            flash(f"Recipe photo upload Successfully!")
            
            if Dosage and UnitName and MyIngredient:
                #we can begin to add ingredients
                print(f"before {IngredientList}")
                add_ingredients_to_list(Dosage,UnitName,MyIngredient)
                print(IngredientList)
                Contents = take_ingredientList_into_str()
                print(f"after {IngredientList}")
                flash(f"added ingredient {MyIngredient} successfully!")
            
            button4 = request.form.get('button4')
            if button4 != None:
                file2 = request.files['file2']
                if file2 != None:
                    file_data = file2
                    #Savelist["image_datas2"] = file_data

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

            #recipe_id = db.session.query(func.max(Recipestep.step_no)).first()
            #Recipes.query.filter_by(id = recipe_id).first()
            no_list = []
            obj = Recipestep.query.filter_by(recipe_id = Savelist["RecipeId"]).all()
            for o in obj:
                no_list.append(int(o.step_no))
            print(no_list)
            if Savelist["Step_number"] != None and (int(Savelist["Step_number"]) in no_list) and (button4 != None):
                flash("Aleady complete this step") 
            elif Savelist["Step_number"] and Savelist["Step_Des"] and Savelist["image_name2"] and (button4 != None):
                
                # we can begin to add steps
                print(f"step + {StepDes}, No. + {StepNo}")
                #get the latest id of this recipeName
                #obj = Recipes.query.filter_by(name = Savelist["RecipeId"]).all()
                recipe_id = Savelist["RecipeId"]
                print("begin to add to db")
                print(f"Step des {StepDes}")
                new_step = Recipestep(recipe_id = recipe_id, step_no = StepNo, step_comment = StepDes, photo = Savelist["image_name2"])
                db.session.add(new_step)
                db.session.commit()             # Commits changes
                flash(f"Added comment at Step.{StepNo}!")
            if (Savelist["Step_number"] != -1) and Savelist["Step_Des"] and (Savelist["image_name2"] == None) and (button4 != None):
                flash(f"Please upload photo for steps!")
            if (Savelist["Step_number"] == -1) and Savelist["Step_Des"] and (Savelist["image_name2"] == None) and (button4 != None):
                flash(f"Please add Step Number!")
            if (Savelist["Step_number"] != -1) and (Savelist["Step_Des"] == None) and (Savelist["image_name2"] == None) and (button4 != None):
                flash(f"Please add Step Description!")

        else:
            flash(f"Please create the recipe first!")


        
        Submit = request.form.get('Submit')
        if Submit != None:
            recipe_id = Savelist["RecipeId"]
            print(Savelist["RecipeId"])
            recipe_data = Recipes.query.filter_by(id = recipe_id).first()
            if recipe_data.photo == None:
                flash(f"Please upload photo for recipe")
            else:
                #get the latest id of this recipeName
                #obj = Recipes.query.filter_by(name= Savelist["RecipeName"]).all()
                #recipe_id = obj[-1].id
                #Savelist["RecipeId"] = recipe_id
                add_ingredient_to_db(recipe_id)
                #fetch description from db
                Description = Recipes.query.filter_by(id = recipe_id).first().description
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
                print(step_list)
                print(image_list)
                print("Yeeeeeea")
                #image_datas1_read = Savelist["image_datas1"].read()
                #image_datas2_read = Savelist["image_datas2"].read()
                #image1 = base64.b64encode(image_datas1_read).decode('ascii')
                #image2 = base64.b64encode(image_datas2_read).decode('ascii')
                
                print(recipe_data.photo)
                image1 = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': recipe_data.photo})
                print(image1)

                Contents = take_ingredientList_into_str()
                IngredientList.clear()#reset
                print("reset2")
                print(IngredientList)
                #IngredientList.clear()
                return redirect(url_for('recipes.view_recipe',recipeName = recipe_data.name,recipeId = recipe_data.id ))
                """return render_template("recipe.html", user=current_user, Descriptions=Description, 
                    RecipeName = Savelist["RecipeName"], MyIngredient = Contents,IngreContents = Contents, 
                    Step1 = step_list[0], Step2 = step_list[1], Step3 = step_list[2], Step4 = step_list[3],
                    image2 = image_list[0], image3 = image_list[1], image4 = image_list[2], image5 = image_list[3], 
                    recipe_id = recipe_id, image1=image1)"""
            Step_No = None
            Step_Number = 0
            if Savelist["RecipeId"]:
                Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
            print("Step_No:")
            print(Step_No)
            if Step_No != None:
                if Step_No[0] != None:
                    Step_Number = Step_No[0]
                else:
                    Step_Number = 0
            else:
                Step_Number = 0
            return render_template("create_recipe.html", user=current_user, IngreContents = Contents, Step_Number = (Step_Number+1))

        else:
            #get the latest id of this recipeName
            
            print("NOooooo")
            Step_No = None
            Step_Number = 0
            if Savelist["RecipeId"]:
                Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
            print("Step_No:")
            print(Step_No)
            if Step_No != None:
                if Step_No[0] != None:
                    Step_Number = Step_No[0]
                else:
                    Step_Number = 0
            else:
                Step_Number = 0
            return render_template("create_recipe.html", user=current_user, IngreContents = Contents, Step_Number = (Step_Number+1))

    else:
        Step_No = None
        Step_Number = 0
        if Savelist["RecipeId"]:
            Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
        print("Step_No:")
        print(Step_No)
        if Step_No != None:
            if Step_No[0] != None:
                Step_Number = Step_No[0]
            else:
                Step_Number = 0
        else:
            Step_Number = 0
        return render_template("create_recipe.html", user=current_user, IngreContents = Contents, Step_Number = (Step_Number+1))
        #return render_template("create_recipe.html", user=current_user)




@recipes.route('/edit recipe', methods = ['GET', 'POST'])
def edit_recipe():
    recipe_id = Savelist["RecipeId"]
    print(recipe_id)
    recipe = Recipes.query.filter_by(id=recipe_id).first()
        
        #find recipe success
    Contents = generate_ingreStr_by_recipeId(recipe.id)
    #RecipeImage = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': recipe.photo})
    #fetch steps from db
    Steps = ""
    obj = Recipestep.query.filter_by(recipe_id = recipe.id).all()
    if request.method == 'POST':
        print("in edit recipe")
        
        
    
        RecipeName = request.form.get('Recipe Name')
        Description = request.form.get('Recipe Des')
        Serving = request.form.get('Servings')
        Dosage = request.form.get('dosage')
        UnitName = request.form.get('Unit Name')
        MyIngredient = request.form.get('Ingredient Name')
        StepNo = request.form.get('step_number')
        StepDes = request.form.get('discriptions')
        Meal_type = request.form.get('Meal type')
        Baking = request.form.get('Baking')
        Frying = request.form.get('Frying')
        Grilling = request.form.get('Grilling')
        Steaming = request.form.get('Steaming')
        Braising = request.form.get('Braising')
        Stewing = request.form.get('Stewing')

        button_create = request.form.get('create')
        if button_create != None:
            '''
            Savelist["Serving"] = Serving
            Savelist["RecipeName"] = RecipeName
            Savelist["Number"] = Number
            Savelist["Dosage"] = Dosage
            Savelist["UnitName"] = UnitName
            Savelist["MyIngredient"] = MyIngredient
            '''
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
    
             
        button3 = request.form.get('button3')
        if button3 != None:
            file1 = request.files['file1']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file1 != None:
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
                    db.session.commit()

                    Savelist["image_name1"] = filename
                    
                    if recipe_data.photo != None:
                        flash(f"Recipe photo updated Successfully!")

        button1 = request.form.get('button1')
        if button1 != None:
            if Savelist["edit_ingredient"] == False:
                ingre = Ingredient.query.filter_by(recipe_id=recipe_id).all()
                for i in ingre:
                    if i.recipe_id == recipe_id:
                        db.session.delete(i)
                db.session.commit()
                Savelist["edit_ingredient"] = True
                IngredientList.clear()
                
            #ingre = Ingredient.query.filter_by(recipe_id=recipeId, dosage=Dosage, unit_name=UnitName, ingredient=MyIngredient).first()
            if Dosage and UnitName and MyIngredient:
                #we can begin to add ingredients
                add_ingredients_to_list(Dosage,UnitName,MyIngredient)
                Contents = take_ingredientList_into_str()

                flash(f"Update ingredient {MyIngredient} successfully!")

        button4 = request.form.get('button4')
        if button4 != None:
            file2 = request.files['file2']
            if file2 != None:
                file_data = file2
                #Savelist["image_datas2"] = file_data

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

            print(no_list)
            if int(Savelist["Step_number"]) not in no_list:
                if StepNo and StepDes and Savelist["image_name2"]:
                    # we can begin to add steps
                    print(f"step + {StepDes}, No. + {StepNo}")
                    #get the latest id of this recipeName
                    #obj = Recipes.query.filter_by(name = Savelist["RecipeId"]).all()
                    recipe_id = Savelist["RecipeId"]
                    print("begin to add to db")
                    print(f"Step des {StepDes}")
                    new_step = Recipestep(recipe_id = recipe_id, step_no = StepNo, step_comment = StepDes, photo = Savelist["image_name2"])
                    db.session.add(new_step)
                    db.session.commit()             # Commits changes
                    flash(f"Added comment at Step.{StepNo}!")

        Submit = request.form.get('Submit')
        if Submit != None:

            #recipe_id = Savelist["RecipeId"]
            print(Savelist["RecipeId"])
            add_ingredient_to_db(recipe_id)
            #fetch description from db
            Description = Recipes.query.filter_by(id = recipe_id).first().description
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
            print(step_list)
            print(image_list)
            print("Yeeeeeea")
            recipe_data = Recipes.query.filter_by(id = recipe_id).first()
            print(recipe_data.photo)
            image1 = s3.generate_presigned_url('get_object', Params={'Bucket': 'comp3900-w18b-sheeesh','Key': recipe_data.photo})
            print(image1)

            Contents = take_ingredientList_into_str()
            IngredientList.clear()
            return redirect(url_for('recipes.view_recipe',recipeName = recipe_data.name,recipeId = recipe_data.id ))
            """return render_template("recipe.html", user=current_user, Descriptions=Description, 
                RecipeName = recipe_data.name, MyIngredient = Contents,IngreContents = Contents, 
                Step1 = step_list[0], Step2 = step_list[1], Step3 = step_list[2], Step4 = step_list[3],
                image2 = image_list[0], image3 = image_list[1], image4 = image_list[2], image5 = image_list[3], 
                recipe_id = recipe_data.id, image1=image1)"""
        else:
            #get the latest id of this recipeName
            print("NOooooo")
            Step_No = None
            Step_Number = 0
            if Savelist["RecipeId"]:
                Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
            print("Step_No:")
            print(Step_No)
            if Step_No != None:
                if Step_No[0] != None:
                    Step_Number = Step_No[0]
                else:
                    Step_Number = 0
            else:
                Step_Number = 0
            return render_template("edit_recipe.html", user=current_user, IngreContents = Contents, recipe = recipe, Step_Number = (Step_Number+1))

    else:
        Step_No = None
        Step_Number = 0
        if Savelist["RecipeId"]:
            Step_No = db.session.query(func.max(Recipestep.step_no)).filter_by(recipe_id = Savelist["RecipeId"]).first()
        print("Step_No:")
        print(Step_No)
        if Step_No != None:
            if Step_No[0] != None:
                Step_Number = Step_No[0]
            else:
                Step_Number = 0
        else:
            Step_Number = 0
        return render_template("edit_recipe.html", user=current_user, IngreContents = Contents, recipe = recipe, Step_Number = (Step_Number+1))
        #return render_template("create_recipe.html", user=current_user)

    
@recipes.route('/<recipeName>.<int:recipeId>', methods=['GET', 'POST'])
def view_recipe(recipeName, recipeId):
    Savelist["edit_ingredient"] = False
    recipe = Recipes.query.filter_by(id=recipeId).first()
    print(recipe)
    if recipe is None:
        flash("No recipe exists with this name and id.", category="error")
        return redirect(url_for('views.home'))

    #find recipe success
    Contents = generate_ingreStr_by_recipeId(recipe.id)
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
    comments = retrieve_comments(recipe.id)
    
    methods = Method.query.filter_by(recipe_id=Savelist["RecipeId"]).all()

    #Create recipe view history
    exist_history = History.query.filter_by(userid = current_user.id, recipe = recipeId).first()
    if exist_history != None:
        print("duplicate browsing")
        date = datetime.date(datetime.now())
        time = datetime.time(datetime.now())
        exist_history.last_view_time = time
        exist_history.last_view_date = date
        db.session.commit()
    else:
        history = History(userid = current_user.id, recipe = recipe.id)
        db.session.add(history)
        db.session.commit()

    return render_template("recipe.html", user=current_user, RecipeName=recipe.name, Descriptions=recipe.description,MyIngredient = Contents,
    recipe_id = recipe.id,image1 = RecipeImage, query = obj, comments=comments, creates = recipe.creates, recipe=recipe, type="recent", meal_type = recipe.meal_type, methods=methods)
        



@recipes.route('/Delete recipe', methods=['GET', 'POST'])
def delete_recipe():
    #delete the recipe using recipeId
    recipe_id = Savelist["RecipeId"]
    #delete ingredient
    ingre = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    for i in ingre:
        if i.recipe_id == recipe_id:
            db.session.delete(i)
    db.session.commit()
    #delete steps
    steps = Recipestep.query.filter_by(recipe_id=recipe_id).all()
    for s in steps:
        if s.recipe_id == recipe_id:
            db.session.delete(s)
    db.session.commit()
    #delete recipe
    recipe = Recipes.query.filter_by(id=recipe_id).first()
    print(recipe.id)
    db.session.delete(recipe)
    db.session.commit()
    return render_template("delete_recipe.html",user = current_user)



#############helper funcs##########
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def create_recipe (RecipeName, Description, Serving, Meal_type):
    #add name and description to db
    print("Begin to add to recipe table")
    user = Profiles.query.filter_by(owns = current_user.id).first()

    new_recipe = Recipes(name = RecipeName, description = Description, 
        serving = Serving, creates = current_user.id, creator = user.first_name, meal_type=Meal_type)

    
    db.session.add(new_recipe)
    db.session.commit()             # Commits changes
    
    
    recipe_id = db.session.query(func.max(Recipes.id)).first()
    print(recipe_id[0])
    Savelist["RecipeId"] = new_recipe.id
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
        Contents += (f"{counter}) --> {Dosage} {UnitName} {MyIngredient}.     "
                    f" ")
        counter += 1
    return Contents

def check_create(RecipeName,userid):
    print(f"name {RecipeName} + {userid}")
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
