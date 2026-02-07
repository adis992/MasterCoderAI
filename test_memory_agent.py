#!/usr/bin/env python3
"""
🧠 MEMORY AGENT TEST - SIMPLE STANDALONE TEST 🧠
"""

import sys
import os
import sqlite3
import asyncio
from datetime import datetime

# Add backend to path
sys.path.insert(0, '/root/MasterCoderAI/backend')

class SimpleMemoryAgent:
    def __init__(self):
        self.memory_db = '/root/MasterCoderAI/backend/memory.db'
        self._init_db()
    
    def _init_db(self):
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance_score REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Memory database initialized!")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    async def health_check(self):
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM memories')
            total_memories = cursor.fetchone()[0]
            conn.close()
            
            return {
                'status': 'healthy',
                'database_connected': True,
                'total_memories_stored': total_memories,
                'last_check': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'database_connected': False,
                'error': str(e)
            }
    
    async def store_memory(self, user_id: int, content: str, memory_type: str = 'test'):
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memories (user_id, memory_type, content, importance_score)
                VALUES (?, ?, ?, ?)
            ''', (user_id, memory_type, content, 0.8))
            
            memory_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'memory_id': memory_id,
                'message': 'Memory stored successfully!'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

async def test_memory_agent():
    print("🧠 Testing Memory Agent...")
    
    agent = SimpleMemoryAgent()
    
    # Test health check
    print("\n1️⃣ Health Check:")
    health = await agent.health_check()
    print(f"Status: {health['status']}")
    print(f"Total memories: {health.get('total_memories_stored', 0)}")
    
    # Test storing memory
    print("\n2️⃣ Storing Test Memory:")
    result = await agent.store_memory(1, "This is a test memory for the brutal AI system!", "test")
    print(f"Store result: {result}")
    
    # Test health check again
    print("\n3️⃣ Health Check After Storage:")
    health = await agent.health_check()
    print(f"Status: {health['status']}")
    print(f"Total memories: {health.get('total_memories_stored', 0)}")
    
    print("\n✅ Memory Agent test completed!")

if __name__ == "__main__":
    asyncio.run(test_memory_agent())