from flask import Blueprint, render_template, request, redirect
from flask import current_app as app
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import check_password_hash
from app.user import User
from replit import db
from app.errors import Errors

# Initialize objects
login_blueprint = Blueprint('login_blueprint', __name__, template_folder = 'templates')
e = Errors()
# login_manager.login_view = 'login' 

# Return login form on direct to /login
@login_blueprint.route('/login')
def login():
  return render_template("login.html")

@login_blueprint.route('/logout')
@login_required
def logout():
  # Logout user and redirect to index, where user can sign up or log in
  logout_user()
  return redirect("/")

@login_blueprint.route("/loginsubmit", methods=["GET", "POST"])
def loginsubmit():
  # If method is post, get info from form and perform checks to see if user is valid
  if request.method == "POST":
    username = request.form.get("username");
    password = request.form.get("password");
    # If username in db, return hashed password. If not, return error
    if username in db.keys():
      dpassword = db[username]
      # If unhashed password is equal to hashed password, login user and define next. If not, return error
      if check_password_hash(dpassword, password):
        user = User(username)
        login_user(user)
        next = request.args.get('next')
        return redirect("/" or next)
      else:
        return render_template("error.html", error = e.wrong_password())
    else:
      return render_template("error.html", error = e.invalid_signup())