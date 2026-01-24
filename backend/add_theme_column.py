#!/usr/bin/env python3
"""
Add 'theme' column to user_settings table
"""
import sqlite3

DB_PATH = "data.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(user_settings)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'theme' not in columns:
        print("🔧 Adding 'theme' column to user_settings...")
        cursor.execute("""
            ALTER TABLE user_settings 
            ADD COLUMN theme TEXT DEFAULT 'matrix'
        """)
        conn.commit()
        print("✅ 'theme' column added!")
    else:
        print("✅ 'theme' column already exists")
    
    conn.close()

if __name__ == "__main__":
    migrate()
