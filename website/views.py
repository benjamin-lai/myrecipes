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
from .models import Images, Users
from . import db

import base64

'''
t_host = "127.0.0.1:5000"
t_port = "5432"
t_dbname = "rec"
t_name_user = "user name"
t_password = 'huzhibo8294'
#data_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_name_user, password=t_password)
#data_cursor = data_conn.cursor()
'''

UPLOAD_FOLDER = 'C:\comp3900\project_data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint('views', __name__)
CORS(views)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/recipe', methods = ['GET','POST'])
def recipe():
    file_data = Images.query.filter_by(username="User 4").first()
    image = base64.b64encode(file_data.image_data).decode('ascii')
    #image = base64.b64encode(file_data.image_data)
    #user = Users.query.filter_by(email=email).first()
    ##file_data = Images.query.filter_by(username="User 1").first()
    #print(file_data.image_name)
    #print(file_data.image_data)
    print("a")
    print("k")
    print(image)
    return render_template("recipe.html", user=current_user, data=list, image=image)


@views.route('/Create recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'POST':
        recipe_name = request.form.get('Recipe Name')
        print(recipe_name)
        serving = request.form.get('Servings')
        print(serving)
        Number = request.form.get('No.')
        print(Number)
        unit = request.form.get('unit')
        print(unit)
        unit_name = request.form.get('Unit Name')
        print(unit_name)
        ingredient_name = request.form.get('Ingredient Name')
        print(ingredient_name)
        Step_number = request.form.get('step_number')
        print(Step_number)
        discriptions = request.form.get('discriptions')
        print(discriptions)

        button1 = request.form.get('button1')
        if button1 != None:
            print(button1)
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
            ##################
            #id_item = 52
            # Pass both item ID and image file data to a function
            #SaveToDatabase(id_item, file)
            print("print file below")
            ##print(file.read())
            print("print file above")
            newFile=Images(
                image_name=filename,
                username="User 4",
                image_data=file.read()
            )
            db.session.add(newFile)
            db.session.commit()

            ##################
            #return render_template("recipe.html", user=current_user)

    
    button3 = request.form.get('button3')
    label = 0
    if button3 != None:
        label = 1
        #print(button3)
        #file_data = Images.query.filter_by(username="User 3").first()
        image = base64.b64encode(file.read()).decode('ascii')
        print("a")
        print("k")
        #print(image)
        return render_template("recipe.html", user=current_user, data=list, image=image)


        #return render_template("recipe.html", user=current_user)
    
    return render_template("create_recipe.html", user=current_user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def SaveToDatabase(id_item, FileImage):
    s = ""
    s += "INSERT INTO Images"
    s += "("
    s += "id_item"
    s += ", blob_file"
    s += ") VALUES ("
    s += "(%id_item)"
    s += ", '(%FileImage)'"
    s += ")"
    # We recommend adding TRY here to trap errors.
    #data_cursor.execute(s, [id_item, FileImage])
    # Use commit here if you do not have auto-commits turned on in PostgreSQL.