# Importing necessary libraries
import os
import sys
import logging
from decouple import config
from flask import Flask,send_from_directory, render_template
from flask_cors import CORS
from flask_migrate import Migrate

from .database import db
from .models import Search, Product, Store, StorePrice
from .routes import prices_bp

# Initializing the Flask app and configuring CORS
def create_app(testing: bool = False):
    
    app = Flask(__name__, static_folder="../frontend/build", static_url_path='/')
    CORS(app)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = config('SECRET_KEY', default='dev_key')
    debug_mode = config('FLASK_DEBUG', default='False', cast=bool)

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL').replace("postgres://", "postgresql://")

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Initialize the database with this app and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # Registering the blueprint
    app.register_blueprint(prices_bp)
    
    return app


app = create_app()

print(app.config['SQLALCHEMY_DATABASE_URI'])



@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    return send_from_directory(app.static_folder, "index.html")

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
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=debug_mode)
