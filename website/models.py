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
    custom_url = db.Column(db.String(150), unique=True)
    owns = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    photo = db.Column(db.String(150))
    serving = db.Column(db.Integer)
    creates = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.Column(db.String(150))
    num_of_likes = db.Column(db.Integer)
    num_of_dislikes = db.Column(db.Integer)
    meal_type = db.Column(db.String(150))

    def __init__(self,name,description,serving,creates, creator, meal_type):
        self.name = name
        self.description = description
        self.photo = None
        self.serving = serving
        self.creates = creates
        self.creator = creator
        self.num_of_likes = 0
        self.num_of_dislikes = 0
        self.meal_type = meal_type

#Ingredient temp dictionary
#Ingredientslist = []
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

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(10000))
    has = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    owns = db.Column(db.Integer, db.ForeignKey('users.id'))

class Method(db.Model, UserMixin):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    method = db.Column(db.String(150), primary_key=True)

class Meal_Type(db.Model, UserMixin):
     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
     meal_type = db.Column(db.String(150), primary_key=True)

# subscriber lists
class Subscriber(db.Model, UserMixin):
    subscriber_id = db.Column(db.Integer, primary_key=True) #initialise to subscriber's id
    contains = db.Column(db.Integer, primary_key=True) # profile (focus)
    
# subscribed to lists
class Subscribed(db.Model, UserMixin):
    subscribed_id = db.Column(db.Integer, primary_key=True) # profile
    contains = db.Column(db.Integer, primary_key=True) # user (focus)
    


# not sure if this is the proper way to add views?
class Newsfeeds(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    photo = db.Column(db.String(150))
    serving = db.Column(db.Integer)
    creates = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.Column(db.String(150))
    contains = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    display_name = db.Column(db.String(150))
    creation_time = db.Column(db.String(150))
    creation_date = db.Column(db.String(150))



class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like_status = db.Column(db.Integer)
    has = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    own = db.Column(db.Integer, db.ForeignKey('users.id'))

class StarredRecipes(db.Model, UserMixin):
    recipe_id = db.Column(db.Integer, primary_key=True) # Recipe
    contains = db.Column(db.Integer, primary_key=True) # User that stars the recipe

# view - A way to access subscriber's profile details
class profile_subs(db.Model, UserMixin):
    profile_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    display_name = db.Column(db.String(150))
    profile_pic = db.Column(db.String(150))
    bio = db.Column(db.String(150))
    custom_url = db.Column(db.String(150), unique=True)
    subscriber_id = db.Column(db.Integer, primary_key=True) #initialise to subscriber's id
    contains = db.Column(db.Integer, primary_key=True) # profile (focus)
    
    
