# File used to create our database models.
from flask_login import UserMixin

from . import db

# IDK what userMixin is but its important for flask-login module
# Just remember you still need to create the tables on your server.
# Refer to schema.sql to compare Users for sqlalchemy and Users for postgresql
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    profile = db.relationship('Profiles', backref='users', lazy=True)
    recipe = db.relationship('Recipes', backref='users', lazy=True)
    
    
# owns is user.id = profile.id, in theory as when the user is made
# the profile should be made at the same time, meaning the ids should be the same 
class Profiles(db.Model, UserMixin):
    profile_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    display_name = db.Column(db.String(150))
    profile_pic = db.Column(db.String(150))
    temp_pic = db.Column(db.String(150))
    bio = db.Column(db.String(150))
    custom_url = db.Column(db.String(150))
    owns = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    photo = db.Column(db.String(150))
    serving = db.Column(db.Integer)
    creates = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.Column(db.String(150))

    def __init__(self,name,description,serving,creates, creator):
        self.name = name
        self.description = description
        self.photo = None
        self.serving = serving
        self.creates = creates
        self.creator = creator

#Ingredient temp dictionary
IngredientList = []
Contents = "empty"

class Ingredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    dosage = db.Column(db.Integer)
    unit_name = db.Column(db.String(150))
    ingredient = db.Column(db.String(150), primary_key=True)

    def __init__(self,recipe_id,dosage,unit_name,ingredient):
        self.recipe_id = recipe_id
        self.dosage = dosage
        self.unit_name = unit_name
        self.ingredient = ingredient
   
class Recipestep(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    step_no = db.Column(db.Integer, primary_key=True)
    step_comment = db.Column(db.String(150))
    photo = db.Column(db.String(150))

    def __init__(self,recipe_id,step_no,step_comment,photo):
        self.recipe_id = recipe_id
        self.step_no = step_no
        self.step_comment = step_comment
        self.photo = photo

class Method(db.Model, UserMixin):
     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
     method = db.Column(db.String(150), primary_key=True)

class Meal_Type(db.Model, UserMixin):
     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
     meal_type = db.Column(db.String(150), primary_key=True)

#contains is profiles.id 
class Subscriber_Lists(db.Model, UserMixin):
    subscriber_id = db.Column(db.Integer, primary_key=True) #initialise to subscriber's id
    contains = db.Column(db.Integer, primary_key=True)
    
    
class Subscribed_To_Lists(db.Model, UserMixin):
    subscribed_id = db.Column(db.Integer, primary_key=True)
    contains = db.Column(db.Integer, primary_key=True)
