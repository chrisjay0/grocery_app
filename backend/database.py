# Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# Initializing the database
db = SQLAlchemy()

# Initializing the database engine
database_url = config('DATABASE_URL').replace("postgres://", "postgresql://")
engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)