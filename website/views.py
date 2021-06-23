# Homepage
from flask import Blueprint, render_template 
from flask_login import  current_user
from flask_cors import CORS

views = Blueprint('views', __name__)
CORS(views)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

