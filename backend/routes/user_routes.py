from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_models import User
from database import db
from models.user_domains import UserDomain

# Create a blueprint for user routes
user_routes = Blueprint('user_routes', __name__)

# Register a new user
@user_routes.route('/user', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Validate the necessary fields
    if not data or not data.get('Username') or not data.get('Email') or not data.get('Password'):
        return jsonify({"error": "Required fields: Username, Email, Password"}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(Email=data['Email']).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400
    
    hashed_password = generate_password_hash(data['Password'], method='sha256')
    
    # Create a new user
    new_user = User(Username=data['Username'], Password=hashed_password, Email=data['Email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# Get a user by ID
@user_routes.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_data = UserDomain(
        UserID=user.UserID,
        Username=user.Username,
        Email=user.Email,
        CreatedDate=user.CreatedDate,
        LastModified=user.LastModified
    )
    return jsonify(user_data), 200

# Update a user by ID
@user_routes.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.filter_by(UserID=user_id).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Update user details (assuming we are only allowing updates to Username and Email for simplicity)
    if data.get('Username'):
        user.Username = data['Username']
    if data.get('Email'):
        user.Email = data['Email']
    
    db.session.commit()
    
    return jsonify({"message": "User updated successfully"}), 200

# Delete a user by ID
@user_routes.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200
