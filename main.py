from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from user import User
from replit import db
from flask_bcrypt import Bcrypt
import errors as e

# Define and initialize all apps
app = Flask(__name__, template_folder='templates')
app.secret_key = b'yWXuzVPlWUT0j0s4APynXBrJAQzWOrEb'
navigation = {'Home':'/', 'Logout':'/logout'}
bcrypt = Bcrypt()
bcrypt.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Manage logins
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Helper function to clear db
def clear():
  for i in db.keys():
    del db[i]

# Index route
@app.route('/')
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
    return render_template("login.html")

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
  # Logout user and redirect to index, where user can sign up or log in
  logout_user()
  return redirect("/")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/loginsubmit", methods=["GET", "POST"])
def loginsubmit():
  # If method is post, get info from form and perform checks to see if user is valid
  if request.method == "POST":
    username = request.form.get("username");
    password = request.form.get("password");
    # If username in db, return hashed password. If not, return error
    if username in db.keys():
      dpassword = db[username]
      # If unhashed password is equal to hashed password, login user and define next. If not, return error
      if bcrypt.check_password_hash(dpassword, password):
        user = User(username)
        login_user(user)
        next = request.args.get('next')
        return redirect("/" or next)
      else:
        return render_template("error.html", error = e.wrong_password)
    else:
      return render_template("error.html", error = e.invalid_signup)

@app.route("/createaccount", methods=["GET", "POST"])
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
        return render_template("error.html", error = e.invalid_char)
    if newusername in db.keys():
      return render_template("error.html", error = e.username_taken)
    if newusername == "":
      return render_template("error.html", error = e.null_username)
    if newpassword == "":
      return render_template("error.html", error = e.null_password)
    db[newusername] = bcrypt.generate_password_hash(newpassword).decode('utf-8')
    user = User(newusername)
    login_user(user)
    next = request.args.get('next')
    return redirect("/" or next)

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=81)