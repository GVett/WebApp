class Errors():
  """
  Errors class to raise certain function and return error message to user
  """
  def __init__(self):
    self.wrong_password = "Wrong password."
    self.invalid_signup = "Account not found."
    self.username_taken = "Username taken."
    self.null_username = "Please enter a username."
    self.null_password = "Please enter a password."
    self.invalid_char = "Username can only contain alphanumeric characters and underscores."

  def wrong_password(self):
    return self.wrong_password

  def invalid_signup(self):
    return self.invalid_signup

  def username_taken(self):
    return self.username_taken

  def null_username(self):
    return self.null_username

  def null_password(self):
    return self.null_password

  def invalid_char(self):
    return self.invalid_char