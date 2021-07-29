# Backend for the homepage.
from flask import Blueprint, render_template
from flask_login import  current_user
from flask_cors import CORS

from .models import Recipes, Profiles


views = Blueprint('views', __name__)
CORS(views)

@views.route('/', methods=['GET', 'POST'])
def home():
    recipe = Recipes.query.all()
    if current_user.is_authenticated is True:
        user = Profiles.query.filter_by(owns = current_user.id).first()
        return render_template("home.html", user=current_user, res = recipe, userName = user.first_name)
    return render_template("home.html", user=current_user, res = recipe)
    




