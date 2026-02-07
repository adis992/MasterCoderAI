"""
🗄️ CREATE MODEL CONFIG TABLE - BRUTALNA DATABASE EXTENSION 🗄️
Database migracija za model konfiguracije
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)

def create_model_config_table():
    """
    📊 CREATE USER MODEL CONFIG TABLE
    """
    try:
        conn = sqlite3.connect('/root/MasterCoderAI/backend/data.db')
        cursor = conn.cursor()
        
        # Create user_model_config table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_model_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                capabilities TEXT DEFAULT '{}',
                capability_settings TEXT DEFAULT '{}',
                agent_preferences TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id)
            )
        ''')
        
        # Create agent_logs table for tracking agent usage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                agent_type TEXT NOT NULL,
                action TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                success BOOLEAN DEFAULT TRUE,
                execution_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create agent_settings table for individual agent configurations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                agent_type TEXT NOT NULL,
                settings TEXT DEFAULT '{}',
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, agent_type)
            )
        ''')
        
        # Create thinking_sessions table for thinking agent logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS thinking_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id TEXT NOT NULL,
                complexity_score REAL,
                thinking_steps TEXT,
                final_response TEXT,
                total_tokens_used INTEGER,
                processing_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Model config tables created successfully!")
        print("✅ Database tables for model configuration created!")
        
    except Exception as e:
        logger.error(f"❌ Database table creation error: {e}")
        print(f"❌ Error creating database tables: {e}")

if __name__ == "__main__":
    create_model_config_table()