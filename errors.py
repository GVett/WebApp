from flask import render_template
from main import app, db

wrong_password = "Wrong password."
invalid_signup = "Account not found."
username_taken = "Username taken."
null_username = "Please enter a username."
null_password = "Please enter a password."
invalid_char = "Username can only contain alphanumeric characters and underscores."