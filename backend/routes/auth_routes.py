from flask import Blueprint, request, jsonify, session
from flask_bcrypt import generate_password_hash, check_password_hash
from models.user_models import User
from database import db

CURR_USER_KEY = "curr user"

auth_bp = Blueprint('auth_bp', __name__)

def do_login(user):
    session[CURR_USER_KEY] = user.UserID

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@auth_bp.route("/user", methods=["POST"])
def signup():
    """Handle user signup."""
    
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    
    # Simple validation (you can add more complex validation later)
    if not username or not password or not email:
        return jsonify({"error": "All fields are required"}), 400
    
    # Check if the user already exists
    user = User.query.filter_by(Username=username).first()
    if user:
        return jsonify({"error": "Username already taken"}), 400

    user = User.query.filter_by(Email=email).first()
    if user:
        return jsonify({"error": "Email already taken"}), 400
    
    # Hash the password and create the user
    hashed_pwd = generate_password_hash(password, 12).decode("utf-8")
    new_user = User(Username=username, Password=hashed_pwd, Email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Handle user login."""
    
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "Both username and password are required"}), 400
    
    user = User.query.filter_by(Username=username).first()
    
    if not user or not check_password_hash(user.Password, password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    do_login(user)

    return jsonify({"message": "Logged in successfully", "user": user.Username}), 200

@auth_bp.route("/logout", methods=["GET"])
def logout():
    """Handle user logout."""
    
    session.pop(CURR_USER_KEY, None)
    return jsonify({"message": "Logged out successfully"}), 200