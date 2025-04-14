"""
Inventory Management System - Database Configuration
"""
import os
from sqlmodel import SQLModel, create_engine, Session

# Define the database file path
DB_FILE = "inventory.db"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILE)

# Create SQLite URL
SQLITE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(SQLITE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db():
    """Initialize the database and create tables if they don't exist"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a new database session"""
    with Session(engine) as session:
        yield session 