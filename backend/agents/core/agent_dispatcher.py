"""
🤖 MASTER AGENT DISPATCHER SYSTEM 🤖
Automatski bira odgovarajućeg agenta na osnovu korisničkog pitanja
Ima permisije na sve i koordinira sav rad
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

from ..email.email_agent import EmailAgent
from ..viber.viber_agent import ViberAgent  
from ..calendar.calendar_agent import CalendarAgent
from ..tasks.task_agent import TaskAgent
from ..web.web_agent import WebAgent
from ..files.file_agent import FileAgent
from ..thinking.thinking_agent import ThinkingAgent
from ..memory.memory_agent import MemoryAgent

logger = logging.getLogger(__name__)

class AgentDispatcher:
    """
    🎯 BRUTALNI AGENT DISPATCHER 🎯
    - Automatski detektuje tip zadatka
    - Bira odgovarajućeg agenta
    - Koordinira rad između agenata
    - Ima admin permisije na sve
    """
    
    def __init__(self):
        self.agents = {
            'email': EmailAgent(),
            'viber': ViberAgent(), 
            'calendar': CalendarAgent(),
            'task': TaskAgent(),
            'web': WebAgent(),
            'file': FileAgent(),
            'thinking': ThinkingAgent(),
            'memory': MemoryAgent()
        }
        
        # 🔥 AGENT KEYWORDS - za detekciju tipa zadatka
        self.agent_keywords = {
            'thinking': [
                'think', 'analyze', 'reason', 'step by step', 'complex', 'solve',
                'razmisli', 'analiziraj', 'objasni', 'korak po korak', 'rezonuj'
            ],
            'email': [
                'email', 'e-mail', 'mail', 'pošta', 'posta', 'send email', 'sendmail',
                'inbox', 'outbox', 'gmail', 'outlook', 'termin', 'appointment', 'meeting'
            ],
            'viber': [
                'viber', 'message', 'poruka', 'chat', 'whatsapp', 'messenger',
                'send message', 'reply', 'odgovori', 'pošalji poruku'
            ],
            'calendar': [
                'calendar', 'kalendar', 'schedule', 'raspored', 'appointment', 'termin',
                'meeting', 'sastanak', 'reminder', 'podsetnik', 'event', 'događaj',
                'today', 'tomorrow', 'danas', 'sutra', 'next week', 'sledeca nedelja'
            ],
            'task': [
                'task', 'zadatak', 'todo', 'create task', 'napravi zadatak',
                'remind me', 'podsetimi', 'remember', 'upamti', 'note', 'beleška'
            ],
            'web': [
                'search', 'pretrage', 'google', 'find', 'pronađi', 'website', 'web',
                'url', 'link', 'browse', 'internet', 'online', 'information about', 
                'latest news', 'current events', 'research', 'what is happening',
                'informacije o', 'poslednje vesti', 'trenutna dešavanja'
            ],
            'file': [
                'file', 'fajl', 'document', 'dokument', 'save', 'sačuvaj', 'open',
                'otvori', 'create file', 'napravi fajl', 'upload', 'download'
            ],
            'memory': [
                'remember', 'zapamti', 'forget', 'zaboravi', 'memory', 'memorija',
                'recall', 'setiti se', 'my profile', 'preferences', 'what did I say',
                'conversation history', 'previously', 'ranije', 'profile', 'profil'
            ]
        }
        
        # 🎯 PRIORITY MATRIX - neki agenti imaju prioritet
        self.priority_order = ['thinking', 'memory', 'email', 'calendar', 'viber', 'task', 'web', 'file']
        
        logger.info("🤖 Agent Dispatcher initialized with brutal efficiency!")
    
    async def dispatch(self, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 GLAVNA DISPATCH FUNKCIJA
        Analizira input i automatski bira odgovarajućeg agenta
        """
        try:
            logger.info(f"🔍 Analyzing user input: {user_input[:100]}...")
            
            # 1. Detektuj tip zadatka
            detected_agents = self._detect_agent_type(user_input)
            
            if not detected_agents:
                # Fallback na general assistant
                return {
                    'success': True,
                    'agent_type': 'general',
                    'response': 'Nisam siguran koji agent treba. Možete precizirati?',
                    'suggestions': ['Email operations', 'Calendar events', 'Viber messages', 'Task management']
                }
            
            # 2. Uzmi najprioritenije agenta
            primary_agent = detected_agents[0]
            
            logger.info(f"🎯 Selected agent: {primary_agent}")
            
            # 3. Pozovi odgovarajućeg agenta
            result = await self._execute_agent(primary_agent, user_input, user_context)
            
            # 4. Ako treba koordinacija između više agenata
            if len(detected_agents) > 1:
                result['multi_agent'] = True
                result['coordinated_agents'] = detected_agents
                
                # Pokreni ostale agente u background-u ako treba
                for agent_type in detected_agents[1:]:
                    asyncio.create_task(
                        self._execute_agent_background(agent_type, user_input, user_context)
                    )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent dispatch error: {e}")
            return {
                'success': False,
                'error': str(e),
                'agent_type': 'error'
            }
    
    def _detect_agent_type(self, user_input: str) -> List[str]:
        """
        🔍 DETEKTUJE KOJI AGENT TREBA
        Koristi keyword matching + priority logic + exclusion filters
        """
        input_lower = user_input.lower()
        
        # 🚫 EXCLUSION FILTERS - Prevent unnecessary web searches
        simple_conversational = [
            'how are you', 'kako si', 'hello', 'hi', 'zdravo', 'hey',
            'good morning', 'dobro jutro', 'good evening', 'dobro veče',
            'thank you', 'hvala', 'thanks', 'bye', 'goodbye', 'doviđenja',
            'what is your name', 'kako se zoveš', 'who are you', 'ko si ti',
            'how do you feel', 'šta osećaš', 'are you okay', 'da li si dobro'
        ]
        
        # Skip web search for simple conversational queries
        is_simple_conversation = any(phrase in input_lower for phrase in simple_conversational)
        
        agent_scores = {}
        
        # Score svaki agent
        for agent_type, keywords in self.agent_keywords.items():
            # Skip web agent for simple conversational queries
            if agent_type == 'web' and is_simple_conversation:
                continue
                
            score = 0
            for keyword in keywords:
                if keyword in input_lower:
                    # Veći score za duže keywords
                    score += len(keyword) * input_lower.count(keyword)
            
            if score > 0:
                agent_scores[agent_type] = score
        
        # Sortiraj po score-u i priority
        detected = []
        for agent_type in self.priority_order:
            if agent_type in agent_scores:
                detected.append(agent_type)
        
        # Dodaj ostale ako nisu u priority
        for agent_type, score in sorted(agent_scores.items(), key=lambda x: x[1], reverse=True):
            if agent_type not in detected:
                detected.append(agent_type)
        
        logger.info(f"🎯 Agent scores: {agent_scores}")
        logger.info(f"🎯 Detection result: {detected}")
        logger.info(f"🚫 Simple conversation filter: {is_simple_conversation}")
        
        return detected
    
    async def _execute_agent(self, agent_type: str, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        ⚡ EXECUTES SPECIFIC AGENT
        """
        try:
            agent = self.agents.get(agent_type)
            if not agent:
                return {
                    'success': False, 
                    'error': f'Agent {agent_type} not found',
                    'agent_type': agent_type
                }
            
            # Execute agent sa full context
            result = await agent.execute(user_input, user_context)
            result['agent_type'] = agent_type
            result['timestamp'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent {agent_type} execution error: {e}")
            return {
                'success': False,
                'error': str(e),
                'agent_type': agent_type
            }
    
    async def _execute_agent_background(self, agent_type: str, user_input: str, user_context: Dict[str, Any]):
        """
        🔄 Background agent execution
        """
        try:
            result = await self._execute_agent(agent_type, user_input, user_context)
            logger.info(f"🔄 Background agent {agent_type} completed: {result.get('success')}")
        except Exception as e:
            logger.error(f"❌ Background agent {agent_type} error: {e}")
    
    def get_available_agents(self) -> Dict[str, Any]:
        """
        📋 RETURNS INFO O SVIM DOSTUPNIM AGENTIMA
        """
        agents_info = {}
        for agent_type, agent in self.agents.items():
            agents_info[agent_type] = {
                'name': agent.__class__.__name__,
                'description': getattr(agent, 'description', f'{agent_type.title()} Agent'),
                'capabilities': getattr(agent, 'capabilities', []),
                'status': 'active'
            }
        
        return {
            'total_agents': len(agents_info),
            'agents': agents_info,
            'dispatch_keywords': self.agent_keywords
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        🩺 HEALTH CHECK ZA SVE AGENTE
        """
        health_status = {}
        
        for agent_type, agent in self.agents.items():
            try:
                if hasattr(agent, 'health_check'):
                    status = await agent.health_check()
                else:
                    status = {'status': 'unknown', 'message': 'No health check implemented'}
                
                health_status[agent_type] = status
                
            except Exception as e:
                health_status[agent_type] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return {
            'dispatcher_status': 'healthy',
            'agents_health': health_status,
            'timestamp': datetime.now().isoformat()
        }

# 🎯 GLOBAL DISPATCHER INSTANCE
dispatcher = AgentDispatcher()