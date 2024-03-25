from flask import Blueprint, render_template, redirect
from flask_login import login_required
from app.navigation import navigation
import urllib.request
import json

movie_blueprint = Blueprint('movie_blueprint', __name__, template_folder = 'templates')

@movie_blueprint.route('/movie')
@login_required
def movie():
  url = "https://api.themoviedb.org/3/discover/movie?api_key=47a3a40c4fe87e48606abbbc69c490c0"

  response = urllib.request.urlopen(url)
  data = response.read()
  dict = json.loads(data)

  return render_template ("movie.html", movies=dict["results"], navigation = navigation)