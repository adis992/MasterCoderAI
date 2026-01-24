#!/usr/bin/env python3
# backend/api/init_db.py
"""
Database Initialization Script
Kreira tabele i dodaje default admin korisnika
"""
import asyncio
import sys
import os

# Fix imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import database, engine, metadata
from api.models import users, user_settings
from werkzeug.security import generate_password_hash

async def init_database():
    """Initialize database with tables and default admin user"""
    print("🔧 Initializing database...")
    
    # Create all tables
    from api.models import users, user_settings  # Import to register tables
    metadata.create_all(engine)
    print("✅ Tables created")
    
    # Connect to database
    await database.connect()
    print("✅ Connected to database")
    
    try:
        # Check if admin user exists
        query = users.select().where(users.c.username == "admin")
        existing_admin = await database.fetch_one(query)
        
        if not existing_admin:
            # Create default admin user
            hashed_pw = generate_password_hash("admin")
            insert_query = users.insert().values(
                username="admin",
                hashed_password=hashed_pw,
                is_admin=True
            )
            admin_id = await database.execute(insert_query)
            print(f"✅ Admin user created (ID: {admin_id})")
            
            # Create default settings for admin
            settings_query = user_settings.insert().values(
                user_id=admin_id,
                active_model="default",
                temperature=0.7,
                max_tokens=2048,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1
            )
            await database.execute(settings_query)
            print("✅ Admin settings created")
        else:
            print("ℹ️  Admin user already exists")
        
        # Create demo user
        demo_query = users.select().where(users.c.username == "user")
        existing_demo = await database.fetch_one(demo_query)
        
        if not existing_demo:
            hashed_pw = generate_password_hash("user123")
            insert_query = users.insert().values(
                username="user",
                hashed_password=hashed_pw,
                is_admin=False
            )
            user_id = await database.execute(insert_query)
            print(f"✅ Demo user created (ID: {user_id})")
            
            # Create default settings for demo user
            settings_query = user_settings.insert().values(
                user_id=user_id,
                active_model="default",
                temperature=0.7,
                max_tokens=2048,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1
            )
            await database.execute(settings_query)
            print("✅ Demo user settings created")
        else:
            print("ℹ️  Demo user already exists")
            
    finally:
        await database.disconnect()
        print("✅ Database initialization complete!")
        print("\n📋 Login credentials:")
        print("   Admin: username=admin, password=admin")
        print("   User:  username=user, password=user123")

if __name__ == "__main__":
    asyncio.run(init_database())
