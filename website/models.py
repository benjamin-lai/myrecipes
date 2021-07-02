# File used to create our database models.
from flask_login import UserMixin

from . import db

# IDK what userMixin is but its important for flask-login module
# Just remember you still need to create the tables on your server.
# Refer to schema.sql to compare Users for sqlalchemy and Users for postgresql
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Images(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    image_name = db.Column(db.String(300))
    image_data = db.Column(db.BLOB)
    username = db.Column(db.String(15))

'''
class Recipe(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(300))
    image = db.Column(db.BLOB)
    creates = db.Column(db.Integer)
'''

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    photo = db.Column(db.String(150))
    serving = db.Column(db.Integer)
    creates = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,name,description,photo,serving,creates):
        self.name = name
        self.description = description
        self.photo = photo
        self.serving = serving
        self.creates = creates


#Ingredient temp dictionary
IngredientList = []

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
