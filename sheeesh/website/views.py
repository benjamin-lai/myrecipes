from flask import Blueprint, render_template
from flask_cors import CORS

views = Blueprint('views', __name__)
CORS(views)

@views.route('/')
def home():
    return render_template("home.html")


