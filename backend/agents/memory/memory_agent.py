"""
🧠 MEMORY AGENT - BRUTALNI MEMORY MANAGEMENT 🧠
- Long-term conversation memory
- Context preservation across sessions
- Smart memory retrieval and storage  
- Personalized user profiling
- Memory optimization and cleanup
"""

import asyncio
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import json
import hashlib

logger = logging.getLogger(__name__)

class MemoryAgent:
    """
    🧠 BRUTALNI MEMORY AGENT 🧠
    Long-term memory storage and intelligent retrieval
    """
    
    def __init__(self):
        self.description = "Advanced Memory Management & Context Preservation Agent"
        self.capabilities = [
            "Long-term conversation memory",
            "Context preservation across sessions",
            "Smart memory retrieval",
            "User preference learning",
            "Conversation summarization", 
            "Memory optimization",
            "Personal profile building",
            "Context-aware responses"
        ]
        
        # Memory configuration
        self.memory_config = {
            'enabled': True,
            'max_memory_entries': 10000,
            'memory_retention_days': 365,
            'auto_summarize': True,
            'context_window': 50,  # Previous messages to consider
            'importance_threshold': 0.6,
            'smart_retrieval': True
        }
        
        # Memory types and importance scores
        self.memory_types = {
            'user_preference': 0.9,
            'personal_info': 0.95,
            'task_completion': 0.7,
            'conversation_topic': 0.5,
            'system_interaction': 0.3,
            'error_handling': 0.6,
            'learning_moment': 0.8
        }
        
        # Initialize memory database
        self.memory_db = self._init_memory_db()
        
        logger.info("🧠 Memory Agent initialized with intelligent storage!")
    
    def _init_memory_db(self) -> str:
        """
        🗄️ INITIALIZE MEMORY DATABASE
        """
        db_path = '/root/MasterCoderAI/backend/memory.db'
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create memories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context TEXT,
                    importance_score REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    accessed_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP,
                    tags TEXT,
                    summary TEXT,
                    related_memories TEXT
                )
            ''')
            
            # Create user profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    preferences TEXT,
                    communication_style TEXT,
                    expertise_areas TEXT,
                    common_tasks TEXT,
                    last_interaction TIMESTAMP,
                    total_conversations INTEGER DEFAULT 0
                )
            ''')
            
            # Create memory embeddings table (for semantic search)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_embeddings (
                    memory_id INTEGER,
                    embedding BLOB,
                    FOREIGN KEY (memory_id) REFERENCES memories (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Memory database initialized: {db_path}")
            return db_path
            
        except Exception as e:
            logger.error(f"❌ Memory DB initialization error: {e}")
            return ""
    
    async def execute(self, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 GLAVNA MEMORY EXECUTION FUNKCIJA
        """
        try:
            logger.info(f"🧠 Processing memory request: {user_input[:100]}...")
            
            # Parse memory intent
            intent = self._parse_memory_intent(user_input)
            
            if intent['action'] == 'store':
                return await self._store_memory(intent, user_context)
            elif intent['action'] == 'retrieve':
                return await self._retrieve_memories(intent, user_context)
            elif intent['action'] == 'profile':
                return await self._get_user_profile(intent, user_context)
            elif intent['action'] == 'forget':
                return await self._forget_memories(intent, user_context)
            elif intent['action'] == 'summarize':
                return await self._summarize_memories(intent, user_context)
            else:
                return await self._general_memory_help(intent, user_context)
                
        except Exception as e:
            logger.error(f"❌ Memory agent error: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': ['Check memory settings', 'Verify database connection', 'Try again later']
            }
    
    def _parse_memory_intent(self, user_input: str) -> Dict[str, Any]:
        """
        🔍 PARSES MEMORY INTENT FROM USER INPUT
        """
        input_lower = user_input.lower()
        
        intent = {
            'action': 'retrieve',  # Default action
            'memory_type': 'conversation_topic',
            'query': user_input,
            'time_range': 'recent',
            'importance_filter': None
        }
        
        # Detect action
        if any(word in input_lower for word in ['remember', 'save', 'store', 'zapamti', 'sačuvaj']):
            intent['action'] = 'store'
        elif any(word in input_lower for word in ['forget', 'delete', 'remove', 'zaboravi', 'obriši']):
            intent['action'] = 'forget'
        elif any(word in input_lower for word in ['profile', 'about me', 'my preferences', 'profil']):
            intent['action'] = 'profile'
        elif any(word in input_lower for word in ['summarize', 'summary', 'overview', 'rezime']):
            intent['action'] = 'summarize'
        elif any(word in input_lower for word in ['recall', 'what did', 'tell me about', 'setiti se']):
            intent['action'] = 'retrieve'
        
        # Detect memory type
        if any(word in input_lower for word in ['preference', 'like', 'prefer', 'volim']):
            intent['memory_type'] = 'user_preference'
        elif any(word in input_lower for word in ['name', 'age', 'personal', 'lično']):
            intent['memory_type'] = 'personal_info'
        elif any(word in input_lower for word in ['task', 'work', 'project', 'zadatak']):
            intent['memory_type'] = 'task_completion'
        
        # Detect time range
        if any(word in input_lower for word in ['today', 'danas']):
            intent['time_range'] = 'today'
        elif any(word in input_lower for word in ['yesterday', 'juče']):
            intent['time_range'] = 'yesterday'
        elif any(word in input_lower for word in ['week', 'nedelja']):
            intent['time_range'] = 'week'
        elif any(word in input_lower for word in ['month', 'mesec']):
            intent['time_range'] = 'month'
        
        return intent
    
    async def _store_memory(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        💾 STORE MEMORY IN DATABASE
        """
        try:
            user_id = user_context.get('user_id', 1)
            memory_content = intent.get('query', '')
            memory_type = intent.get('memory_type', 'conversation_topic')
            
            # Calculate importance score
            importance_score = self._calculate_importance(memory_content, memory_type)
            
            # Generate context and tags
            context = json.dumps(user_context)
            tags = self._extract_tags(memory_content)
            
            # Store in database
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memories 
                (user_id, memory_type, content, context, importance_score, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, memory_type, memory_content, context, importance_score, tags))
            
            memory_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Update user profile
            await self._update_user_profile(user_id, memory_content, memory_type)
            
            return {
                'success': True,
                'memory_stored': {
                    'id': memory_id,
                    'type': memory_type,
                    'content': memory_content[:200] + '...' if len(memory_content) > 200 else memory_content,
                    'importance_score': importance_score,
                    'tags': tags.split(',') if tags else []
                },
                'message': f"Memory stored successfully with importance score {importance_score:.2f}",
                'actions': [
                    'View stored memories',
                    'Update memory importance',
                    'Add related memories',
                    'Create memory summary'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Store memory error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _retrieve_memories(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        🔍 RETRIEVE RELEVANT MEMORIES
        """
        try:
            user_id = user_context.get('user_id', 1)
            query = intent.get('query', '')
            memory_type = intent.get('memory_type')
            time_range = intent.get('time_range', 'recent')
            
            # Build SQL query based on filters
            sql_conditions = ['user_id = ?']
            params = [user_id]
            
            if memory_type:
                sql_conditions.append('memory_type = ?')
                params.append(memory_type)
            
            # Time range filter
            if time_range == 'today':
                sql_conditions.append("DATE(created_at) = DATE('now')")
            elif time_range == 'yesterday':
                sql_conditions.append("DATE(created_at) = DATE('now', '-1 day')")
            elif time_range == 'week':
                sql_conditions.append("created_at >= datetime('now', '-7 days')")
            elif time_range == 'month':
                sql_conditions.append("created_at >= datetime('now', '-30 days')")
            else:  # recent
                sql_conditions.append("created_at >= datetime('now', '-7 days')")
            
            # Execute query
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            sql = f'''
                SELECT id, memory_type, content, importance_score, created_at, tags
                FROM memories 
                WHERE {' AND '.join(sql_conditions)}
                ORDER BY importance_score DESC, created_at DESC
                LIMIT 20
            '''
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            # Update access count
            if results:
                memory_ids = [str(row[0]) for row in results]
                cursor.execute(f'''
                    UPDATE memories 
                    SET accessed_count = accessed_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE id IN ({','.join(['?'] * len(memory_ids))})
                ''', memory_ids)
                conn.commit()
            
            conn.close()
            
            # Format results
            memories = []
            for row in results:
                memories.append({
                    'id': row[0],
                    'type': row[1],
                    'content': row[2],
                    'importance_score': row[3],
                    'created_at': row[4],
                    'tags': row[5].split(',') if row[5] else []
                })
            
            # Rank by relevance to current query
            if query and memories:
                memories = self._rank_by_relevance(memories, query)
            
            return {
                'success': True,
                'memories_found': len(memories),
                'memories': memories,
                'search_query': query,
                'filters_applied': {
                    'memory_type': memory_type,
                    'time_range': time_range
                },
                'actions': [
                    'View memory details',
                    'Update memory importance',
                    'Delete selected memories',
                    'Export memories'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Retrieve memories error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _get_user_profile(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        👤 GET USER PROFILE AND PREFERENCES
        """
        try:
            user_id = user_context.get('user_id', 1)
            
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # Get user profile
            cursor.execute('''
                SELECT name, preferences, communication_style, expertise_areas, 
                       common_tasks, last_interaction, total_conversations
                FROM user_profiles WHERE user_id = ?
            ''', (user_id,))
            
            profile_result = cursor.fetchone()
            
            # Get memory statistics
            cursor.execute('''
                SELECT 
                    memory_type,
                    COUNT(*) as count,
                    AVG(importance_score) as avg_importance
                FROM memories 
                WHERE user_id = ?
                GROUP BY memory_type
                ORDER BY count DESC
            ''', (user_id,))
            
            memory_stats = cursor.fetchall()
            conn.close()
            
            # Format profile
            if profile_result:
                profile = {
                    'name': profile_result[0],
                    'preferences': json.loads(profile_result[1]) if profile_result[1] else {},
                    'communication_style': profile_result[2],
                    'expertise_areas': json.loads(profile_result[3]) if profile_result[3] else [],
                    'common_tasks': json.loads(profile_result[4]) if profile_result[4] else [],
                    'last_interaction': profile_result[5],
                    'total_conversations': profile_result[6]
                }
            else:
                profile = {
                    'name': None,
                    'preferences': {},
                    'communication_style': 'neutral',
                    'expertise_areas': [],
                    'common_tasks': [],
                    'last_interaction': None,
                    'total_conversations': 0
                }
            
            # Format memory statistics
            memory_breakdown = {}
            for stat in memory_stats:
                memory_breakdown[stat[0]] = {
                    'count': stat[1],
                    'average_importance': round(stat[2], 2)
                }
            
            return {
                'success': True,
                'user_profile': profile,
                'memory_statistics': memory_breakdown,
                'total_memories': sum(stat['count'] for stat in memory_breakdown.values()),
                'profile_completeness': self._calculate_profile_completeness(profile),
                'actions': [
                    'Update profile preferences',
                    'Set communication style',
                    'Add expertise areas',
                    'Export profile data'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Get user profile error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_importance(self, content: str, memory_type: str) -> float:
        """
        📊 CALCULATE MEMORY IMPORTANCE SCORE
        """
        base_score = self.memory_types.get(memory_type, 0.5)
        
        # Content length factor
        length_factor = min(len(content) / 1000, 1.0) * 0.2
        
        # Keyword importance
        important_keywords = ['important', 'remember', 'always', 'never', 'prefer', 'like', 'dislike']
        keyword_score = sum(0.1 for keyword in important_keywords if keyword in content.lower())
        
        final_score = min(base_score + length_factor + keyword_score, 1.0)
        return round(final_score, 2)
    
    def _extract_tags(self, content: str) -> str:
        """
        🏷️ EXTRACT TAGS FROM CONTENT
        """
        # Simple tag extraction (in real implementation would use NLP)
        common_tags = ['work', 'personal', 'preference', 'task', 'meeting', 'code', 'project']
        found_tags = [tag for tag in common_tags if tag in content.lower()]
        return ','.join(found_tags)
    
    def _rank_by_relevance(self, memories: List[Dict], query: str) -> List[Dict]:
        """
        🎯 RANK MEMORIES BY RELEVANCE TO QUERY
        """
        query_words = set(query.lower().split())
        
        for memory in memories:
            content_words = set(memory['content'].lower().split())
            overlap = len(query_words.intersection(content_words))
            memory['relevance_score'] = overlap / len(query_words) if query_words else 0
        
        return sorted(memories, key=lambda x: (x['relevance_score'], x['importance_score']), reverse=True)
    
    def _calculate_profile_completeness(self, profile: Dict) -> float:
        """
        📈 CALCULATE PROFILE COMPLETENESS PERCENTAGE
        """
        completeness = 0.0
        
        if profile['name']:
            completeness += 0.2
        if profile['preferences']:
            completeness += 0.3
        if profile['communication_style'] != 'neutral':
            completeness += 0.2
        if profile['expertise_areas']:
            completeness += 0.15
        if profile['common_tasks']:
            completeness += 0.15
        
        return round(completeness * 100, 1)
    
    async def _update_user_profile(self, user_id: int, content: str, memory_type: str):
        """
        👤 UPDATE USER PROFILE BASED ON NEW MEMORY
        """
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # Check if profile exists
            cursor.execute('SELECT total_conversations FROM user_profiles WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            
            if result:
                # Update existing profile
                new_conversation_count = result[0] + 1
                cursor.execute('''
                    UPDATE user_profiles 
                    SET total_conversations = ?, last_interaction = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (new_conversation_count, user_id))
            else:
                # Create new profile
                cursor.execute('''
                    INSERT INTO user_profiles (user_id, total_conversations, last_interaction)
                    VALUES (?, 1, CURRENT_TIMESTAMP)
                ''', (user_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Update user profile error: {e}")
    
    async def _general_memory_help(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ❓ GENERAL MEMORY HELP
        """
        return {
            'success': True,
            'message': "Memory Agent ready for intelligent memory management! 🧠",
            'available_actions': [
                'Store important information',
                'Retrieve past conversations',
                'View user profile',
                'Manage memory preferences',
                'Summarize conversation history',
                'Forget specific memories'
            ],
            'examples': [
                "Remember that I prefer morning meetings",
                "What did we discuss about the project last week?",
                "Show my profile and preferences",
                "Summarize our recent conversations"
            ],
            'memory_types': list(self.memory_types.keys()),
            'current_config': self.memory_config
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        🩺 MEMORY AGENT HEALTH CHECK
        """
        try:
            # Test database connection
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM memories')
            total_memories = cursor.fetchone()[0]
            conn.close()
            
            return {
                'status': 'healthy',
                'database_connected': True,
                'total_memories_stored': total_memories,
                'memory_enabled': self.memory_config['enabled'],
                'capabilities_active': len(self.capabilities),
                'last_check': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Memory health check error: {e}")
            return {
                'status': 'degraded',
                'database_connected': False,
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }