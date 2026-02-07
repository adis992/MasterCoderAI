#!/usr/bin/env python3
"""
Migration script - Dodaje nove kolone u user_settings tabelu
DeepLearning, Opinion, VSCode i Web Search postavke
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'api', 'data.db')

def migrate_database():
    """Dodaj nove kolone u user_settings tabelu"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔄 Starting database migration...")
    
    # Nove kolone za dodavanje
    new_columns = [
        ("deeplearning_intensity", "REAL DEFAULT 0.8"),
        ("deeplearning_context", "REAL DEFAULT 1.0"),
        ("deeplearning_memory", "REAL DEFAULT 0.9"),
        ("opinion_confidence", "REAL DEFAULT 0.7"),
        ("opinion_creativity", "REAL DEFAULT 0.8"),
        ("opinion_critical_thinking", "REAL DEFAULT 0.9"),
        ("vscode_auto_open", "BOOLEAN DEFAULT 0"),
        ("vscode_permissions", "VARCHAR(20) DEFAULT 'full'"),
        ("auto_web_search", "BOOLEAN DEFAULT 1"),
        ("web_search_threshold", "REAL DEFAULT 0.7"),
    ]
    
    for column_name, column_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE user_settings ADD COLUMN {column_name} {column_type}")
            print(f"✅ Added column: {column_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"⚠️  Column {column_name} already exists - skipping")
            else:
                print(f"❌ Error adding {column_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print("✅ Migration completed successfully!")
    print("\n📊 New columns added:")
    print("  🧠 DeepLearning: intensity, context, memory")
    print("  🎭 Opinion: confidence, creativity, critical_thinking")
    print("  💻 VSCode: auto_open, permissions")
    print("  🌐 Web Search: auto_web_search, threshold")

if __name__ == "__main__":
    migrate_database()
