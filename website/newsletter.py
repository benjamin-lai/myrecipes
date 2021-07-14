from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from flask_cors import CORS

from . import db
from .models import Users, Profiles, Newsfeeds


newsletter = Blueprint('newsletter', __name__)
CORS(newsletter)

@newsletter.route('/manage_newsletters', methods=['GET', 'POST'])
def manage_newsletter():
    if request.method == 'POST':
        # Getting list of integers, that correspond to content they want in their newsletters
        selected = request.form.getlist('checkbox')
        print(selected)
        

        

    return render_template("newsletters.html", user=current_user)
