from sqlalchemy import Column, Integer, String, Boolean, MetaData, Table

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_admin", Boolean, default=False),
    Column("last_token", String, nullable=True)
)
