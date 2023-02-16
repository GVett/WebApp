from flask import Blueprint, render_template, redirect
from flask_login import current_user
from replit import db
from app.navigation import navigation

home_blueprint = Blueprint('gome_blueprint', __name__, template_folder = 'templates')

@home_blueprint.route('/')
def index():
  # Define user and check if authenticated
  user = current_user
  loggedIn = user.is_authenticated
  # If logged in, return username and greet user on log in
  if loggedIn:
    username = user.return_username()
    if username != None and username in db.keys():
      return render_template("index.html", navigation = navigation, username = username)
    else:
      return redirect("/logout")
  # If not logged in, return login form
  else:
    return redirect("/login")