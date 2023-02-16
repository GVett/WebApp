from flask import Blueprint, render_template, request, redirect
from flask import current_app as app
from flask_login import login_user
from flask_bcrypt import generate_password_hash
from app.user import User
from replit import db
from app.errors import Errors

# Initialize objects
signup_blueprint = Blueprint('signup_blueprint', __name__, template_folder = 'templates')
e = Errors()

@signup_blueprint.route("/signup")
def signup():
    return render_template("signup.html")

@signup_blueprint.route("/createaccount", methods=["GET", "POST"])
def createaccount():
  # If method is post, get info from form and perform checks to see if new user is valid
  if request.method == "POST":
    newusername = request.form.get("newusername")
    newpassword = request.form.get("newpassword")
    # Set valid characters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    cap_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    allchars = letters + cap_letters + numbers + ['_']
    # Perform various checks and return errors if true. If not, sign in new user and store new user in db
    for i in newusername:
      if i not in allchars:
        return render_template("error.html", error = e.invalid_char())
    if newusername in db.keys():
      return render_template("error.html", error = e.username_taken())
    if newusername == "":
      return render_template("error.html", error = e.null_username())
    if newpassword == "":
      return render_template("error.html", error = e.null_password())
    # Store username/password pair in database
    db[newusername] = generate_password_hash(newpassword).decode('utf-8')
    user = User(newusername)
    login_user(user)
    # Prevent redirects
    next = request.args.get('next')
    return redirect("/" or next)