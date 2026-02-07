#!/usr/bin/env python3
"""
🌐 AGENT DISPATCHER TEST - TEST CONVERSATIONAL FILTERING 🌐
"""

import sys
import asyncio

# Add backend to path
sys.path.insert(0, '/root/MasterCoderAI/backend')

class SimpleDispatcher:
    def __init__(self):
        self.agent_keywords = {
            'thinking': [
                'think', 'analyze', 'reason', 'step by step', 'complex', 'solve',
                'razmisli', 'analiziraj', 'objasni', 'korak po korak', 'rezonuj'
            ],
            'memory': [
                'remember', 'zapamti', 'forget', 'zaboravi', 'memory', 'memorija',
                'recall', 'setiti se', 'my profile', 'preferences', 'what did I say',
                'conversation history', 'previously', 'ranije', 'profile', 'profil'
            ],
            'web': [
                'search', 'pretrage', 'google', 'find', 'pronađi', 'website', 'web',
                'url', 'link', 'browse', 'internet', 'online', 'information about', 
                'latest news', 'current events', 'research', 'what is happening',
                'informacije o', 'poslednje vesti', 'trenutna dešavanja'
            ]
        }
        
        self.priority_order = ['thinking', 'memory', 'web']
    
    def _detect_agent_type(self, user_input: str):
        """Test agent detection with exclusion filters"""
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
        
        return {
            'detected_agents': detected,
            'agent_scores': agent_scores,
            'is_simple_conversation': is_simple_conversation
        }

async def test_dispatcher():
    print("🤖 Testing Agent Dispatcher...")
    
    dispatcher = SimpleDispatcher()
    
    # Test queries
    test_queries = [
        "how are you?",
        "kako si ti?",
        "hello there!",
        "search for python tutorials",
        "remember my name is John",
        "analyze this complex problem step by step",
        "find information about AI",
        "thank you for your help",
        "what is happening in the world today"
    ]
    
    for query in test_queries:
        result = dispatcher._detect_agent_type(query)
        print(f"\n📝 Query: '{query}'")
        print(f"   🤖 Detected agents: {result['detected_agents']}")
        print(f"   📊 Agent scores: {result['agent_scores']}")
        print(f"   🚫 Simple conversation: {result['is_simple_conversation']}")
    
    print("\n✅ Dispatcher test completed!")

if __name__ == "__main__":
    asyncio.run(test_dispatcher())