# The file which will initialise everything relevant for our web application
#   SQLAlchemy, Flask, App configurationos, Blueprints and Login Manager

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# Initialising database and parameters
db = SQLAlchemy()
DB_NAME = "rec"
DB_PASSWORD = 'aa'

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Mail parameters
    app.config.update(
        SECRET_KEY = 'amongus',
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT= 465,
        MAIL_USE_SSL= True,
        MAIL_USERNAME = 'w18b.sheeesh@gmail.com',
        MAIL_PASSWORD = "sheeesh3900"
    )

    # Connects us to our database when we initialise the application.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .profile import profile
    from .Recipe import recipes
    from .newsfeed import newsfeed
    from .review import review
    from .search import search
    from .newsletter import newsletter
    from .support import support
    from .Trending_section import trending_section
    from .history import historys
    from .cookbook import cookbook

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(recipes, url_prefix='/')
    app.register_blueprint(newsfeed, url_prefix='/')
    app.register_blueprint(review, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')
    app.register_blueprint(newsletter, url_prefix='/')
    app.register_blueprint(support, url_prefix='/')
    app.register_blueprint(trending_section, url_prefix='/')
    app.register_blueprint(historys, url_prefix='/')
    app.register_blueprint(cookbook, url_prefix='/profile')
    

    from .models import Users

    # Manages our login
    # Flask redirects us to 'home' when we are not logged in 
    login_manager = LoginManager()
    login_manager.login_view = 'home'
    login_manager.init_app(app)

    # Telling flask how we load a user
    # Looks for primary key and convert it into a int
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app