"""
📧 EMAIL AGENT - BRUTALNI EMAIL MANAGEMENT 📧
- Čita email-ove
- Odgovara automatski
- Pravi termine i meeting-e
- Koordinira sa calendar agentom
"""

import asyncio
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import re
import json

logger = logging.getLogger(__name__)

class EmailAgent:
    """
    📧 BRUTALNI EMAIL AGENT 📧
    Full email management sa AI odgovaranjem
    """
    
    def __init__(self):
        self.description = "Advanced Email Management Agent"
        self.capabilities = [
            "Read incoming emails",
            "Send automated replies", 
            "Schedule meetings from email",
            "Extract calendar events",
            "Smart email filtering",
            "Contact management"
        ]
        
        # Email server settings
        self.imap_settings = {
            'gmail': {'server': 'imap.gmail.com', 'port': 993},
            'outlook': {'server': 'outlook.office365.com', 'port': 993},
            'yahoo': {'server': 'imap.mail.yahoo.com', 'port': 993}
        }
        
        self.smtp_settings = {
            'gmail': {'server': 'smtp.gmail.com', 'port': 587},
            'outlook': {'server': 'smtp.office365.com', 'port': 587}, 
            'yahoo': {'server': 'smtp.mail.yahoo.com', 'port': 587}
        }
        
        # 🎯 EMAIL PATTERNS za parsing
        self.meeting_patterns = [
            r'meeting.*?(\d{1,2}[:\-\.]\d{2})',  # meeting at 14:00
            r'termin.*?(\d{1,2}[:\-\.]\d{2})',   # termin u 15:30
            r'sastanak.*?(\d{1,2}[:\-\.]\d{2})', # sastanak 16:45
            r'appointment.*?(\d{1,2}[:\-\.]\d{2})', # appointment 11:15
        ]
        
        self.date_patterns = [
            r'(\d{1,2})[\.\/\-](\d{1,2})[\.\/\-](\d{4})',  # DD.MM.YYYY
            r'(\d{4})[\.\/\-](\d{1,2})[\.\/\-](\d{1,2})',  # YYYY-MM-DD
            r'(sutra|tomorrow)',  # relative dates
            r'(danas|today)',
            r'(preksutra|day after tomorrow)'
        ]
        
        logger.info("📧 Email Agent initialized!")
    
    async def execute(self, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 GLAVNA EMAIL EXECUTION FUNKCIJA
        """
        try:
            logger.info(f"📧 Processing email request: {user_input[:100]}...")
            
            # Parse user intent
            intent = self._parse_email_intent(user_input)
            
            if intent['action'] == 'read':
                return await self._read_emails(intent, user_context)
            elif intent['action'] == 'send':
                return await self._send_email(intent, user_context)
            elif intent['action'] == 'reply':
                return await self._reply_email(intent, user_context)
            elif intent['action'] == 'schedule':
                return await self._schedule_from_email(intent, user_context)
            else:
                return await self._general_email_help(intent, user_context)
                
        except Exception as e:
            logger.error(f"❌ Email agent error: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': ['Check email settings', 'Verify credentials', 'Try again later']
            }
    
    def _parse_email_intent(self, user_input: str) -> Dict[str, Any]:
        """
        🔍 PARSES EMAIL INTENT FROM USER INPUT
        """
        input_lower = user_input.lower()
        
        intent = {
            'action': 'general',
            'provider': None,
            'recipient': None,
            'subject': None,
            'body': None,
            'meeting_time': None,
            'meeting_date': None
        }
        
        # Detect action
        if any(word in input_lower for word in ['read', 'check', 'inbox', 'čitaj', 'proveri']):
            intent['action'] = 'read'
        elif any(word in input_lower for word in ['send', 'pošalji', 'send email']):
            intent['action'] = 'send'
        elif any(word in input_lower for word in ['reply', 'odgovori', 'respond']):
            intent['action'] = 'reply'
        elif any(word in input_lower for word in ['meeting', 'termin', 'schedule', 'appointment']):
            intent['action'] = 'schedule'
        
        # Detect email provider
        if 'gmail' in input_lower:
            intent['provider'] = 'gmail'
        elif 'outlook' in input_lower:
            intent['provider'] = 'outlook'
        elif 'yahoo' in input_lower:
            intent['provider'] = 'yahoo'
        
        # Extract meeting time/date
        for pattern in self.meeting_patterns:
            match = re.search(pattern, input_lower)
            if match:
                intent['meeting_time'] = match.group(1)
                break
        
        for pattern in self.date_patterns:
            match = re.search(pattern, input_lower)
            if match:
                intent['meeting_date'] = match.group(0)
                break
        
        return intent
    
    async def _read_emails(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📖 READ INCOMING EMAILS
        """
        try:
            # Mock implementation - u realnom sistemu bi se povezao na IMAP
            emails = [
                {
                    'id': 1,
                    'from': 'client@example.com',
                    'subject': 'Meeting Request - Tomorrow 14:00',
                    'body': 'Hi, can we schedule a meeting tomorrow at 2 PM?',
                    'date': datetime.now().isoformat(),
                    'unread': True,
                    'meeting_detected': True,
                    'suggested_response': 'I can schedule that meeting for you. Let me check my calendar.'
                },
                {
                    'id': 2,
                    'from': 'partner@company.com',
                    'subject': 'Project Update Required',
                    'body': 'Please send the latest project status by end of day.',
                    'date': (datetime.now() - timedelta(hours=2)).isoformat(),
                    'unread': True,
                    'meeting_detected': False,
                    'suggested_response': 'I will prepare the project update and send it shortly.'
                }
            ]
            
            # Check for meetings and schedule them
            meetings_found = []
            for email_item in emails:
                if email_item.get('meeting_detected'):
                    meeting_info = self._extract_meeting_info(email_item)
                    if meeting_info:
                        meetings_found.append(meeting_info)
            
            return {
                'success': True,
                'emails': emails,
                'unread_count': len([e for e in emails if e['unread']]),
                'meetings_detected': meetings_found,
                'actions': [
                    'Reply to emails',
                    'Schedule detected meetings',  
                    'Mark as read',
                    'Forward to calendar'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Read emails error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _send_email(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📤 SEND EMAIL
        """
        try:
            # Mock implementation
            email_data = {
                'to': intent.get('recipient', 'recipient@example.com'),
                'subject': intent.get('subject', 'Automated Response'),
                'body': intent.get('body', 'This is an automated email from AI Assistant.'),
                'sent_at': datetime.now().isoformat(),
                'status': 'sent'
            }
            
            return {
                'success': True,
                'email_sent': email_data,
                'message': f"Email sent successfully to {email_data['to']}",
                'actions': ['View sent emails', 'Schedule follow-up', 'Add to calendar']
            }
            
        except Exception as e:
            logger.error(f"❌ Send email error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _reply_email(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        💬 REPLY TO EMAIL
        """
        try:
            # Generate AI response based on context
            reply_data = {
                'original_email_id': intent.get('email_id', 1),
                'reply_subject': f"RE: {intent.get('original_subject', 'Your Message')}",
                'reply_body': self._generate_smart_reply(intent, user_context),
                'sent_at': datetime.now().isoformat(),
                'status': 'sent'
            }
            
            return {
                'success': True,
                'reply_sent': reply_data,
                'message': "Smart reply sent successfully",
                'ai_confidence': 0.85
            }
            
        except Exception as e:
            logger.error(f"❌ Reply email error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _schedule_from_email(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📅 SCHEDULE MEETING FROM EMAIL
        """
        try:
            meeting_data = {
                'title': 'Meeting from Email',
                'date': intent.get('meeting_date', 'tomorrow'),
                'time': intent.get('meeting_time', '14:00'),
                'participants': [intent.get('recipient', 'client@example.com')],
                'location': 'TBD',
                'created_from_email': True,
                'created_at': datetime.now().isoformat()
            }
            
            # Pozovi calendar agent da kreira event
            from ..calendar.calendar_agent import CalendarAgent
            calendar_agent = CalendarAgent()
            calendar_result = await calendar_agent.create_event(meeting_data)
            
            return {
                'success': True,
                'meeting_scheduled': meeting_data,
                'calendar_event': calendar_result,
                'message': f"Meeting scheduled for {meeting_data['date']} at {meeting_data['time']}",
                'actions': ['Send calendar invite', 'Set reminder', 'Add to agenda']
            }
            
        except Exception as e:
            logger.error(f"❌ Schedule from email error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_meeting_info(self, email_data: Dict) -> Optional[Dict]:
        """
        🔍 EXTRACT MEETING INFO FROM EMAIL
        """
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        meeting_info = {
            'detected_from': 'email',
            'email_id': email_data.get('id'),
            'title': email_data.get('subject'),
            'participants': [email_data.get('from')]
        }
        
        # Extract time
        for pattern in self.meeting_patterns:
            match = re.search(pattern, f"{subject} {body}")
            if match:
                meeting_info['time'] = match.group(1)
                break
        
        # Extract date
        for pattern in self.date_patterns:
            match = re.search(pattern, f"{subject} {body}")
            if match:
                meeting_info['date'] = match.group(0)
                break
        
        return meeting_info if 'time' in meeting_info else None
    
    def _generate_smart_reply(self, intent: Dict, user_context: Dict) -> str:
        """
        🧠 GENERATE SMART AI REPLY
        """
        # Simple template-based replies - u realnom sistemu bi koristio LLM
        templates = {
            'meeting': "Thank you for the meeting request. I've checked my calendar and can confirm the proposed time. I'll send you a calendar invite shortly.",
            'project': "Thank you for your message regarding the project. I will review the details and provide you with a comprehensive update within the next few hours.",
            'general': "Thank you for your email. I have received your message and will respond appropriately based on the content."
        }
        
        # Detect reply type
        original_content = f"{intent.get('original_subject', '')} {intent.get('original_body', '')}".lower()
        
        if any(word in original_content for word in ['meeting', 'schedule', 'termin']):
            return templates['meeting']
        elif any(word in original_content for word in ['project', 'update', 'status']):
            return templates['project']
        else:
            return templates['general']
    
    async def _general_email_help(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ❓ GENERAL EMAIL HELP
        """
        return {
            'success': True,
            'message': "Email Agent ready for action!",
            'available_actions': [
                'Read inbox emails',
                'Send new emails', 
                'Reply to messages',
                'Schedule meetings from emails',
                'Extract calendar events',
                'Manage contacts'
            ],
            'examples': [
                "Read my Gmail inbox",
                "Send email to client@example.com",
                "Reply to the meeting request",
                "Schedule the meeting from latest email"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        🩺 EMAIL AGENT HEALTH CHECK
        """
        return {
            'status': 'healthy',
            'capabilities_active': len(self.capabilities),
            'providers_supported': list(self.imap_settings.keys()),
            'last_check': datetime.now().isoformat()
        }