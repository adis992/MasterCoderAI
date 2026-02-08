"""
MasterCoderAI - Database Configuration
Jednostavna SQLite baza - bez komplikacija!
"""
import os
import sqlite3
from databases import Database
from sqlalchemy import create_engine, MetaData

# SQLite baza - jednostavno i efikasno
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

def get_db():
    """Get direct SQLite connection for integrations"""
    db_path = DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    try:
        yield conn
    finally:
        conn.close()
