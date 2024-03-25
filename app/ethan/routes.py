from flask import Blueprint, render_template
from flask_login import login_required
from app.navigation import navigation

ethan_blueprint = Blueprint('ethan_blueprint', __name__, template_folder = 'templates')

@ethan_blueprint.route('/ethan')
@login_required
def ethan():
  return render_template("ethan.html", navigation = navigation)