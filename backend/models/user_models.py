from datetime import datetime
from database import db


# User model
class User(db.Model):
    __tablename__ = "User"

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.Text, nullable=False)  # This will store the hashed password
    Email = db.Column(db.String(255), unique=True, nullable=False)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


# UserPreference model
class UserPreference(db.Model):
    __tablename__ = "UserPreference"

    PreferenceID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(
        db.Integer, db.ForeignKey("User.UserID", ondelete="CASCADE"), nullable=False
    )
    AppSetting = db.Column(db.String(255))
    DietaryPreference = db.Column(db.String(255))
    ZipCode = db.Column(db.String(10))
    MaxTravelDistance = db.Column(db.Float(precision=2))
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user = db.relationship("User", backref="preferences")


# UserProductFavorite model
class UserProductFavorite(db.Model):
    __tablename__ = "UserProductFavorite"

    FavoriteID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(
        db.Integer, db.ForeignKey("User.UserID", ondelete="CASCADE"), nullable=False
    )
    ProductID = db.Column(
        db.Integer, db.ForeignKey("Product.ProductID"), nullable=False
    )
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)
    LastModified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user = db.relationship("User", backref="favorites")
