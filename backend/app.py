# Importing necessary libraries
import logging
from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from database import db
from models import Search, Product, Store, StorePrice
from routes import prices_bp

# Initializing the Flask app and configuring CORS
app = Flask(__name__)
CORS(app)

# Setting up logging
logging.basicConfig(filename='flask_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppresses a warning and potential performance hit
app.config['SECRET_KEY'] = config('SECRET_KEY', default='dev_key')

# Initialize the database with this app and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Registering the blueprint
app.register_blueprint(prices_bp)

@app.route("/", methods=["GET", "POST"])
def show_homepage():
    return 'homepage'

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error("404 error encountered.")
    return '404', 404

@app.errorhandler(403)
def page_not_autherized(e):
    app.logger.error("403 error encountered.")
    return '403', 403

@app.errorhandler(405)
def method_not_allowed(e):
    app.logger.error("405 error encountered.")
    return '405', 405

if __name__ == '__main__':
    app.run(debug=True)
