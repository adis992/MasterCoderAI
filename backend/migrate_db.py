#!/usr/bin/env python3
"""
Database Migration Script
Adds auto_load_model_name column to system_settings table
WITHOUT deleting existing data!
"""
import sqlite3
import sys

def migrate():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(system_settings)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'auto_load_model_name' not in columns:
            print("🔧 Adding auto_load_model_name column...")
            cursor.execute("""
                ALTER TABLE system_settings 
                ADD COLUMN auto_load_model_name TEXT
            """)
            conn.commit()
            print("✅ auto_load_model_name added!")
        else:
            print("✅ auto_load_model_name already exists")
        
        if 'web_search_enabled' not in columns:
            print("🔧 Adding web_search_enabled column...")
            cursor.execute("""
                ALTER TABLE system_settings 
                ADD COLUMN web_search_enabled INTEGER DEFAULT 0
            """)
            conn.commit()
            print("✅ web_search_enabled added!")
        else:
            print("✅ web_search_enabled already exists")
        
        # Verify
        cursor.execute("SELECT * FROM system_settings")
        row = cursor.fetchone()
        print(f"\n📊 Current settings: {row}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
