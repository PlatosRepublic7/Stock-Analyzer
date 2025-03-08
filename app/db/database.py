from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from .env
load_dotenv(find_dotenv())

# Read the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the sqlalchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)