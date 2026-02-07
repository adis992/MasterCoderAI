"""
🌐 WEB AGENT - BRUTALNA WEB SEARCH & AUTOMATION 🌐
- Web pretrage i analiza
- Automated browsing
- Content extraction
- Website monitoring
- API integrations
"""

import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import re
import json
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WebAgent:
    """
    🌐 BRUTALNI WEB AGENT 🌐
    Advanced web search and automation
    """
    
    def __init__(self):
        self.description = "Advanced Web Search & Automation Agent"
        self.capabilities = [
            "Web search and research",
            "Website content extraction",
            "Automated browsing",
            "API integrations",
            "Website monitoring",
            "Data scraping",
            "Link validation",
            "SEO analysis"
        ]
        
        # Search engines and APIs
        self.search_engines = {
            'google': 'https://www.googleapis.com/customsearch/v1',
            'bing': 'https://api.bing.microsoft.com/v7.0/search',
            'duckduckgo': 'https://api.duckduckgo.com/'
        }
        
        # Common headers for web requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        logger.info("🌐 Web Agent initialized!")
    
    async def execute(self, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 GLAVNA WEB EXECUTION FUNKCIJA
        """
        try:
            logger.info(f"🌐 Processing web request: {user_input[:100]}...")
            
            # Parse user intent
            intent = self._parse_web_intent(user_input)
            
            if intent['action'] == 'search':
                return await self._web_search(intent, user_context)
            elif intent['action'] == 'extract':
                return await self._extract_content(intent, user_context)
            elif intent['action'] == 'monitor':
                return await self._monitor_website(intent, user_context)
            elif intent['action'] == 'validate':
                return await self._validate_links(intent, user_context)
            else:
                return await self._general_web_help(intent, user_context)
                
        except Exception as e:
            logger.error(f"❌ Web agent error: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': ['Check URL format', 'Verify internet connection', 'Try different search terms']
            }
    
    def _parse_web_intent(self, user_input: str) -> Dict[str, Any]:
        """
        🔍 PARSES WEB INTENT FROM USER INPUT
        """
        input_lower = user_input.lower()
        
        intent = {
            'action': 'search',
            'query': None,
            'url': None,
            'search_engine': 'google',
            'max_results': 10,
            'language': 'en'
        }
        
        # Detect action
        if any(word in input_lower for word in ['search', 'find', 'look for', 'traži', 'pronađi']):
            intent['action'] = 'search'
        elif any(word in input_lower for word in ['extract', 'scrape', 'get content', 'izvuci']):
            intent['action'] = 'extract'
        elif any(word in input_lower for word in ['monitor', 'watch', 'track', 'prati']):
            intent['action'] = 'monitor'
        elif any(word in input_lower for word in ['validate', 'check links', 'verify', 'proveri']):
            intent['action'] = 'validate'
        
        # Extract URL if present
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, user_input)
        if url_match:
            intent['url'] = url_match.group(0)
        
        # Extract search query
        if intent['action'] == 'search':
            # Remove action words to get clean query
            query = user_input
            for word in ['search', 'find', 'look for', 'traži', 'pronađi', 'google']:
                query = re.sub(rf'\b{word}\b', '', query, flags=re.IGNORECASE)
            intent['query'] = query.strip()
        
        # Detect language
        if any(word in input_lower for word in ['serbian', 'srpski', 'на српском']):
            intent['language'] = 'sr'
        elif any(word in input_lower for word in ['english', 'engleski', 'in english']):
            intent['language'] = 'en'
        
        return intent
    
    async def _web_search(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        🔍 PERFORM WEB SEARCH
        """
        try:
            query = intent.get('query', 'default search')
            max_results = intent.get('max_results', 10)
            
            # Mock search results - u realnom sistemu bi koristio pravi search API
            search_results = [
                {
                    'title': 'How to Build AI Agents - Complete Guide',
                    'url': 'https://example.com/ai-agents-guide',
                    'snippet': 'Learn how to build intelligent AI agents with Python, FastAPI, and machine learning. Step-by-step tutorial with code examples.',
                    'domain': 'example.com',
                    'search_score': 0.95,
                    'published_date': '2024-01-20'
                },
                {
                    'title': 'FastAPI Backend Development Best Practices',
                    'url': 'https://fastapi-guide.com/best-practices',
                    'snippet': 'Comprehensive guide to building scalable backend APIs with FastAPI, including authentication, database integration, and testing.',
                    'domain': 'fastapi-guide.com',
                    'search_score': 0.89,
                    'published_date': '2024-01-18'
                },
                {
                    'title': 'React Frontend Architecture Patterns',
                    'url': 'https://react-patterns.dev/architecture',
                    'snippet': 'Modern React frontend architecture patterns for building maintainable and scalable web applications.',
                    'domain': 'react-patterns.dev',
                    'search_score': 0.83,
                    'published_date': '2024-01-15'
                }
            ]
            
            # Analyze search results
            search_analysis = {
                'total_results': len(search_results),
                'avg_relevance': sum(r['search_score'] for r in search_results) / len(search_results),
                'top_domains': list(set(r['domain'] for r in search_results[:5])),
                'recent_results': len([r for r in search_results if '2024' in r.get('published_date', '')])
            }
            
            return {
                'success': True,
                'query': query,
                'search_results': search_results[:max_results],
                'analysis': search_analysis,
                'search_metadata': {
                    'search_time': datetime.now().isoformat(),
                    'search_engine': intent.get('search_engine', 'google'),
                    'language': intent.get('language', 'en')
                },
                'actions': [
                    'Extract content from links',
                    'Refine search query',
                    'Save results',
                    'Monitor for updates'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Web search error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _extract_content(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📄 EXTRACT WEBSITE CONTENT
        """
        try:
            url = intent.get('url', 'https://example.com')
            
            # Mock content extraction
            extracted_content = {
                'url': url,
                'title': 'Sample Website Title',
                'description': 'Sample website description from meta tags',
                'content': '''
                This is the main content of the webpage. It contains important information 
                about the topic. The content has been cleaned and formatted for easy reading.
                
                Key points from the article:
                - First important point about the topic
                - Second key insight from the content
                - Third valuable information extracted
                ''',
                'word_count': 156,
                'reading_time': '1 min',
                'images': [
                    {'src': 'https://example.com/image1.jpg', 'alt': 'Sample image'},
                    {'src': 'https://example.com/image2.jpg', 'alt': 'Another image'}
                ],
                'links': [
                    {'text': 'Related Article', 'href': 'https://example.com/related'},
                    {'text': 'External Resource', 'href': 'https://external.com/resource'}
                ],
                'metadata': {
                    'author': 'John Doe',
                    'published_date': '2024-01-20',
                    'last_modified': '2024-01-21',
                    'language': 'en',
                    'keywords': ['AI', 'automation', 'development']
                }
            }
            
            return {
                'success': True,
                'extracted_content': extracted_content,
                'content_analysis': {
                    'content_quality': 'high',
                    'readability_score': 85,
                    'seo_score': 78,
                    'mobile_friendly': True
                },
                'actions': [
                    'Save content locally',
                    'Generate summary',
                    'Create task from content',
                    'Share with team'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Extract content error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _monitor_website(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        👁️ MONITOR WEBSITE FOR CHANGES
        """
        try:
            url = intent.get('url', 'https://example.com')
            
            # Mock monitoring setup
            monitoring_config = {
                'url': url,
                'check_frequency': '1 hour',
                'last_check': datetime.now().isoformat(),
                'monitor_id': f"monitor_{datetime.now().timestamp()}",
                'notifications': {
                    'email': True,
                    'viber': True,
                    'calendar_event': False
                },
                'change_detection': {
                    'content_changes': True,
                    'price_changes': False,
                    'availability_changes': False,
                    'new_articles': True
                }
            }
            
            # Mock change detection results
            change_summary = {
                'changes_detected': 2,
                'last_change': (datetime.now() - timedelta(hours=3)).isoformat(),
                'change_types': ['content_update', 'new_link_added'],
                'severity': 'medium'
            }
            
            return {
                'success': True,
                'monitoring_setup': monitoring_config,
                'recent_changes': change_summary,
                'message': f"Website monitoring setup for {url}",
                'actions': [
                    'Configure notifications',
                    'Set change thresholds',
                    'View change history',
                    'Export monitoring report'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Monitor website error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _validate_links(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        🔗 VALIDATE WEBSITE LINKS
        """
        try:
            base_url = intent.get('url', 'https://example.com')
            
            # Mock link validation
            link_validation_results = {
                'total_links_checked': 25,
                'valid_links': 22,
                'broken_links': 3,
                'redirect_links': 5,
                'external_links': 8,
                'internal_links': 17,
                'check_time': datetime.now().isoformat()
            }
            
            broken_links = [
                {
                    'url': 'https://example.com/broken-page',
                    'status_code': 404,
                    'error': 'Page not found',
                    'location': 'Homepage footer'
                },
                {
                    'url': 'https://old-domain.com/resource',
                    'status_code': 500,
                    'error': 'Server error',
                    'location': 'About page'
                }
            ]
            
            return {
                'success': True,
                'validation_results': link_validation_results,
                'broken_links': broken_links,
                'recommendations': [
                    f"Fix {len(broken_links)} broken links",
                    "Review redirect chains",
                    "Update external link references",
                    "Implement link monitoring"
                ],
                'actions': [
                    'Generate detailed report',
                    'Create fix tasks',
                    'Schedule regular checks',
                    'Notify webmaster'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Validate links error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _fetch_url_content(self, url: str) -> Dict[str, Any]:
        """
        📡 FETCH URL CONTENT (helper function)
        """
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    content = await response.text()
                    
                    return {
                        'status_code': response.status,
                        'content': content,
                        'headers': dict(response.headers),
                        'url': str(response.url)
                    }
        except Exception as e:
            return {
                'status_code': 0,
                'error': str(e),
                'content': None
            }
    
    def _extract_text_from_html(self, html_content: str) -> str:
        """
        📄 EXTRACT CLEAN TEXT FROM HTML
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            logger.error(f"❌ HTML text extraction error: {e}")
            return ""
    
    async def _general_web_help(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ❓ GENERAL WEB HELP
        """
        return {
            'success': True,
            'message': "Web Agent ready for browsing! 🌐",
            'available_actions': [
                'Search the web',
                'Extract website content',
                'Monitor websites for changes',
                'Validate website links',
                'Analyze SEO performance',
                'Scrape data from sites'
            ],
            'examples': [
                "Search for AI development tutorials",
                "Extract content from https://example.com",
                "Monitor https://news-site.com for updates",
                "Validate all links on my website"
            ],
            'supported_formats': [
                'HTML websites',
                'JSON APIs',
                'XML feeds',
                'CSS selectors'
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        🩺 WEB AGENT HEALTH CHECK
        """
        # Test basic web connectivity
        test_url = "https://httpbin.org/get"
        connectivity_test = await self._fetch_url_content(test_url)
        
        return {
            'status': 'healthy' if connectivity_test.get('status_code') == 200 else 'degraded',
            'internet_connectivity': connectivity_test.get('status_code') == 200,
            'search_engines_available': len(self.search_engines),
            'capabilities_active': len(self.capabilities),
            'last_check': datetime.now().isoformat()
        }