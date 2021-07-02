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


class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    serving = db.Column(db.Integer)
    creates = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,name,description,serving,creates):
        self.name = name
        self.description = description
        self.serving = serving
        self.creates = creates


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

    def __init__(self,recipe_id,step_no,step_comment):
        self.recipe_id = recipe_id
        self.step_no = step_no
        self.step_comment = step_comment
