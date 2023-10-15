# Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# Initializing the database
db = SQLAlchemy()

# Initializing the database engine

engine = create_engine(config('DATABASE_URL'), echo=True)
Session = sessionmaker(bind=engine)