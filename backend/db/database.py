"""
MasterCoderAI - Database Configuration
Jednostavna SQLite baza - bez komplikacija!
"""
import os
from databases import Database
from sqlalchemy import create_engine, MetaData

# SQLite baza - jednostavno i efikasno
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
