from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "rec"
DB_PASSWORD = 'huzhibo8294'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'amongus'

    # Connects us to our database when we initialise the application.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .profile import profile

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/profile')

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

