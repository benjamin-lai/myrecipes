# Backend for the homepage. Sends recipes into homepage and for the slider.

from flask import Blueprint, render_template
from flask_login import  current_user
from flask_cors import CORS

from .models import Recipes, Profiles, Likes


views = Blueprint('views', __name__)
CORS(views)

@views.route('/', methods=['GET', 'POST'])
def home():
    query = Recipes.query.all()
    #put custom url into recipe list
    recipes = []
    for r in query:
        recipe = Recipes.query.filter_by(id=r.id).first()
        profile = Profiles.query.filter_by(profile_id=recipe.creates).first()
        setattr(recipe, "custom_url", profile.custom_url)
        recipes.append(recipe)
    
    if current_user.is_authenticated is True:
        user = Profiles.query.filter_by(owns = current_user.id).first()
        trend = Likes.query.all()
        LikeList = []
        for t in trend:
            if t.like_status > 0:
                LikeList.append(t.has)
        #limit to 5
        LikeList = LikeList[:5]
        trend = []
        for l in LikeList:
            trend.append(Recipes.query.filter_by(id = l).first())

        #put custom url into recipe list
        trending = []
        for r in trend:
            recipe = Recipes.query.filter_by(id=r.id).first()
            profile = Profiles.query.filter_by(profile_id=recipe.creates).first()
            setattr(recipe, "custom_url", profile.custom_url)
            trending.append(recipe)
        return render_template("home.html", user=current_user, res = recipes, 
        userName = user.first_name,trend = trending)
    return render_template("home.html", user=current_user, res = recipes, trend = recipes[:5])
    




