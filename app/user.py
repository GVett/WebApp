from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin):
    # User object
    def __init__(self, name):
      self._name = name

    def return_username(self):
      return self._name

    def get_id(self):
      return str(self._name)

class AnonUser(AnonymousUserMixin):
    def __init(self):
      self._name = "AnonUser"
  
    def get_id(self):
      return str(self._name)