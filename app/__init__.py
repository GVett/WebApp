import sys
sys.path.append('app')

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .user import User
from home.routes import home_blueprint
from login.routes import login_blueprint
from signup.routes import signup_blueprint

login_manager = LoginManager()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
  return User(user_id)

def create_app():
  app = Flask(__name__)
  app.secret_key = b'yWXuzVPlWUT0j0s4APynXBrJAQzWOrEb'

  login_manager.init_app(app)
  bcrypt.init_app(app)

  app.register_blueprint(home_blueprint)
  app.register_blueprint(login_blueprint)
  app.register_blueprint(signup_blueprint)
    
  return app