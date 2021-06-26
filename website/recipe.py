from flask import Blueprint, render_template 
from flask_login import login_required, current_user
from flask_cors import CORS

recipe = Blueprint('recipe', __name__)
CORS(recipe)
'''
@recipe.route('/recipe', methods=['GET', 'POST'])
@login_required
def recipe():
    return render_template("recipe.html", user=current_user)
'''

