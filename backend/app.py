# Importing necessary libraries
from flask_migrate import Migrate
from flask import Flask
from decouple import config
from flask import g
from flask_cors import CORS
from flask import session


from database import db

from models.product_models import *
from models.user_models import *
from models.store_models import *
from models.searchterm_models import *

from routes.auth_routes import auth_bp
from routes.prices_routes import prices_bp




# Initializing the Flask app
app = Flask(__name__)
CORS(app)

# Registering the blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(prices_bp)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This suppresses a warning and potential performance hit
app.config['SECRET_KEY'] = config('SECRET_KEY', default='dev_key')

# Initialize the database with this app
db.init_app(app)

# Initializing Flask-Migrate
migrate = Migrate(app, db)

CURR_USER_KEY = "curr user"

###########################
## Homepage and error pages

@app.route("/", methods=["GET", "POST"])
def show_homepage():
    return 'homepage'

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return '404', 404

@app.errorhandler(403)
def page_not_autherized(e):
    """403 NOT auth page."""

    return '403', 403

@app.errorhandler(405)
def page_not_autherized(e):
    """405 method not allowed."""

    return '405', 405

###########################
## Login / Logout / Signup Routes

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
    return None


###########################
## Running the app
if __name__ == '__main__':
    app.run(debug=True)
