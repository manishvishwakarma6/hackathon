from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from urllib.parse import quote_plus

 
db = MongoEngine()

# Create a Flask app   
def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    

    # Correctly escaped MongoDB URI
    username = quote_plus('Mediminds')
    password = quote_plus('6Coders@1249')
    host = 'bsr.q22tj85.mongodb.net'
    db_name = 'BSR'
    uri = f"mongodb+srv://{username}:{password}@{host}/{db_name}?retryWrites=true&w=majority&appName=BSR"

    # Set the MONGODB_SETTINGS
    app.config['MONGODB_SETTINGS'] = {
        'host': uri
    }

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.get(id=user_id)
    
    return app
