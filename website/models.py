# File used to create our database models.
from flask_login import UserMixin

from . import db

# IDK what userMixin is but its important for flask-login module
# Just remember you still need to create the tables on your server.
# Refer to schema.sql to compare Users for sqlalchemy and Users for postgresql
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

# owns is user.id = profile.id, in theory as when the user is made
# the profile should be made at the same time, meaning the ids should be the same 
class Profiles(db.Model, UserMixin):
    profile_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    display_name = db.Column(db.String(150))
    profile_pic = db.Column(db.String(150))
    bio = db.Column(db.String(150))
    owns = db.Column(db.Integer)
    
    
class Recipes(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ingredients = db.Column(db.String(150))
    method = db.Column(db.String(150))
    meal_types = db.Column(db.String(150))
    description = db.Column(db.String(150))
    photo = db.Column(db.String(150))
    creates = db.Column(db.Integer)


#contains is profiles.id 
class Subscriber_Lists(db.Model, UserMixin):
    subscriber_id = db.Column(db.Integer, primary_key=True)
    contains = db.Column(db.Integer, primary_key=True)
    
    
class Subscribed_To_Lists(db.Model, UserMixin):
    subscribed_id = db.Column(db.Integer, primary_key=True)
    contains = db.Column(db.Integer, primary_key=True)


    
    