# Profile Page, I haven't done anything that cool yet.
from flask import Blueprint, render_template 
from flask_login import login_required, current_user
from flask_cors import CORS

profile = Blueprint('profile', __name__)
CORS(profile)

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

