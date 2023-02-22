from flask import Blueprint, render_template, redirect
from flask_login import login_required
from replit import db
from app.navigation import navigation

movie_blueprint = Blueprint('movie_blueprint', __name__, template_folder = 'templates')

@movie_blueprint.route('/movie')
@login_required
def movie():
  # Render movie template (EPIC DA RATT MOMENTOOOOOOOOOOO)
  return render_template("movie.html", navigation = navigation)