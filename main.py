from replit import db
from app import create_app

# Clear db helper function
def clear():
  for i in db.keys():
    del db[i]

if __name__ == '__main__':
    """
    Initialize app
    """
  
    app = create_app()
    app.run(host='0.0.0.0', port=81)