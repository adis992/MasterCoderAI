from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from .db import metadata, engine
import datetime

# Users table
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(150), unique=True, index=True),
    Column("hashed_password", String(255)),
    Column("is_admin", Boolean, default=False),
    Column("last_token", String(512), nullable=True)  # Dodano za spremanje zadnjeg tokena
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
    Column("status", String(50), default="pending"),
    Column("created_at", DateTime, default=datetime.datetime.utcnow)
)

# User settings table
user_settings = Table(
    "user_settings", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), unique=True),
    Column("cpu_enabled", Boolean, default=True),
    Column("gpu_enabled", JSON, default=[]),
    Column("temperature", String(10), default="0.7"),
    Column("max_tokens", Integer, default=1024),
    Column("active_model", String(255), nullable=True)
)

# Create tables moved to main.py startup event
# metadata.create_all(engine)