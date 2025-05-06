from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from .db import metadata, engine
import datetime

# Users table
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_admin", Boolean, default=False)
)

# Chats table
chats = Table(
    "chats", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("message", Text),
    Column("response", Text),
    Column("timestamp", DateTime, default=datetime.datetime.utcnow)
)

# Tasks table
tasks = Table(
    "tasks", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("task_data", JSON),
    Column("status", String, default="pending"),
    Column("created_at", DateTime, default=datetime.datetime.utcnow)
)

# Create tables
metadata.create_all(engine)