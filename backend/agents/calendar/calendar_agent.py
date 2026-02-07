"""
📅 CALENDAR AGENT - BRUTALNI KALENDAR MANAGEMENT 📅
- Dnevni kalendar i obavještenja
- Automatsko kreiranje termina
- Meeting scheduling
- Reminder sistem
- Event koordinacija između agenata
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, date
import logging
import json
import re
from calendar import monthrange

logger = logging.getLogger(__name__)

class CalendarAgent:
    """
    📅 BRUTALNI CALENDAR AGENT 📅
    Full calendar management sa daily notifications
    """
    
    def __init__(self):
        self.description = "Advanced Calendar & Event Management Agent"
        self.capabilities = [
            "Daily calendar overview",
            "Event creation and management",
            "Meeting scheduling", 
            "Smart reminders",
            "Recurring events",
            "Time conflict detection",
            "Calendar sync",
            "Notification system"
        ]
        
        # Calendar storage (u realnom sistemu bi bila baza)
        self.events_storage = {}
        
        # 🎯 TIME PATTERNS za parsing
        self.time_patterns = [
            r'(\d{1,2})[:\-\.h](\d{2})',  # 14:30, 14-30, 14.30, 14h30
            r'(\d{1,2})\s*h',             # 14h, 15h  
            r'u\s*(\d{1,2})',             # u 14, u 15
            r'at\s*(\d{1,2})',            # at 14, at 3
        ]
        
        self.date_patterns = [
            r'(\d{1,2})[\.\/\-](\d{1,2})[\.\/\-](\d{4})',  # DD.MM.YYYY
            r'(\d{4})[\.\/\-](\d{1,2})[\.\/\-](\d{1,2})',  # YYYY-MM-DD
            r'(sutra|tomorrow)',                             # relativno
            r'(danas|today)',
            r'(preksutra|day after tomorrow)',
            r'(sledeće nedelje|next week)',
            r'(sledećeg meseca|next month)'
        ]
        
        self.duration_patterns = [
            r'(\d+)\s*(h|hour|hours|sati?)',    # 2h, 3 hours
            r'(\d+)\s*(min|minutes|minuta?)',   # 30min, 45 minutes
            r'ceo\s*dan|whole\s*day',           # ceo dan
            r'pola\s*sata|half\s*hour'          # pola sata
        ]
        
        # Event types i templates
        self.event_types = {
            'meeting': {
                'icon': '🤝',
                'default_duration': 60,  # minutes
                'reminder_before': 15    # minutes
            },
            'call': {
                'icon': '📞', 
                'default_duration': 30,
                'reminder_before': 5
            },
            'task': {
                'icon': '✅',
                'default_duration': 120,
                'reminder_before': 30
            },
            'appointment': {
                'icon': '📋',
                'default_duration': 45,
                'reminder_before': 10
            },
            'reminder': {
                'icon': '⏰',
                'default_duration': 5,
                'reminder_before': 0
            }
        }
        
        logger.info("📅 Calendar Agent initialized!")
    
    async def execute(self, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 GLAVNA CALENDAR EXECUTION FUNKCIJA
        """
        try:
            logger.info(f"📅 Processing calendar request: {user_input[:100]}...")
            
            # Parse user intent
            intent = self._parse_calendar_intent(user_input)
            
            if intent['action'] == 'view':
                return await self._view_calendar(intent, user_context)
            elif intent['action'] == 'create':
                return await self._create_event(intent, user_context)
            elif intent['action'] == 'update':
                return await self._update_event(intent, user_context)
            elif intent['action'] == 'delete':
                return await self._delete_event(intent, user_context)
            elif intent['action'] == 'daily_overview':
                return await self._daily_overview(intent, user_context)
            elif intent['action'] == 'reminders':
                return await self._get_reminders(intent, user_context)
            else:
                return await self._general_calendar_help(intent, user_context)
                
        except Exception as e:
            logger.error(f"❌ Calendar agent error: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': ['Check date format', 'Verify event details', 'Try simpler command']
            }
    
    def _parse_calendar_intent(self, user_input: str) -> Dict[str, Any]:
        """
        🔍 PARSES CALENDAR INTENT FROM USER INPUT
        """
        input_lower = user_input.lower()
        
        intent = {
            'action': 'view',
            'event_title': None,
            'date': None,
            'time': None,
            'duration': None,
            'participants': [],
            'event_type': 'meeting',
            'location': None
        }
        
        # Detect action
        if any(word in input_lower for word in ['create', 'add', 'schedule', 'book', 'napravi', 'dodaj', 'zakaži']):
            intent['action'] = 'create'
        elif any(word in input_lower for word in ['update', 'edit', 'change', 'modify', 'promeni', 'izmeni']):
            intent['action'] = 'update'
        elif any(word in input_lower for word in ['delete', 'remove', 'cancel', 'obriši', 'ukloni', 'otkaži']):
            intent['action'] = 'delete'
        elif any(word in input_lower for word in ['today', 'danas', 'daily', 'dnevno']):
            intent['action'] = 'daily_overview'
        elif any(word in input_lower for word in ['remind', 'reminder', 'notification', 'podsetnik', 'obavesti']):
            intent['action'] = 'reminders'
        elif any(word in input_lower for word in ['view', 'show', 'list', 'prikaži', 'vidi']):
            intent['action'] = 'view'
        
        # Detect event type
        if any(word in input_lower for word in ['call', 'poziv', 'telefonski']):
            intent['event_type'] = 'call'
        elif any(word in input_lower for word in ['task', 'zadatak', 'job']):
            intent['event_type'] = 'task'
        elif any(word in input_lower for word in ['appointment', 'termin']):
            intent['event_type'] = 'appointment'
        elif any(word in input_lower for word in ['reminder', 'podsetnik']):
            intent['event_type'] = 'reminder'
        
        # Extract time
        for pattern in self.time_patterns:
            match = re.search(pattern, input_lower)
            if match:
                if len(match.groups()) == 2:
                    intent['time'] = f"{match.group(1)}:{match.group(2)}"
                else:
                    intent['time'] = f"{match.group(1)}:00"
                break
        
        # Extract date
        for pattern in self.date_patterns:
            match = re.search(pattern, input_lower)
            if match:
                intent['date'] = match.group(0)
                break
        
        # Extract duration
        for pattern in self.duration_patterns:
            match = re.search(pattern, input_lower)
            if match:
                if 'ceo dan' in match.group(0) or 'whole day' in match.group(0):
                    intent['duration'] = 480  # 8 hours
                elif 'pola sata' in match.group(0) or 'half hour' in match.group(0):
                    intent['duration'] = 30
                else:
                    value = int(match.group(1))
                    unit = match.group(2) if len(match.groups()) > 1 else ''
                    if 'h' in unit or 'hour' in unit or 'sat' in unit:
                        intent['duration'] = value * 60
                    else:
                        intent['duration'] = value
                break
        
        return intent
    
    async def _view_calendar(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        👀 VIEW CALENDAR EVENTS
        """
        try:
            target_date = self._parse_date(intent.get('date', 'today'))
            events = self._get_events_for_date(target_date)
            
            return {
                'success': True,
                'date': target_date.isoformat(),
                'events': events,
                'total_events': len(events),
                'busy_hours': self._calculate_busy_hours(events),
                'free_slots': self._find_free_slots(target_date, events),
                'actions': ['Add event', 'Edit event', 'Delete event', 'Set reminder']
            }
            
        except Exception as e:
            logger.error(f"❌ View calendar error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _create_event(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ➕ CREATE NEW EVENT
        """
        try:
            event_date = self._parse_date(intent.get('date', 'today'))
            event_time = intent.get('time', '09:00')
            event_type = intent.get('event_type', 'meeting')
            
            # Generate event ID
            event_id = f"evt_{datetime.now().timestamp()}"
            
            # Default duration from event type
            duration = intent.get('duration') or self.event_types[event_type]['default_duration']
            
            new_event = {
                'id': event_id,
                'title': intent.get('event_title', f'New {event_type.title()}'),
                'date': event_date.isoformat(),
                'time': event_time,
                'duration_minutes': duration,
                'type': event_type,
                'icon': self.event_types[event_type]['icon'],
                'participants': intent.get('participants', []),
                'location': intent.get('location', 'TBD'),
                'reminder_before': self.event_types[event_type]['reminder_before'],
                'created_at': datetime.now().isoformat(),
                'created_by': user_context.get('user_id', 'system')
            }
            
            # Check for conflicts
            conflicts = self._check_conflicts(new_event, event_date)
            
            # Store event
            date_key = event_date.isoformat()
            if date_key not in self.events_storage:
                self.events_storage[date_key] = []
            self.events_storage[date_key].append(new_event)
            
            return {
                'success': True,
                'event_created': new_event,
                'conflicts': conflicts,
                'message': f"Event '{new_event['title']}' created for {event_date.strftime('%d.%m.%Y')} at {event_time}",
                'actions': ['Set reminder', 'Invite participants', 'Add to other calendars']
            }
            
        except Exception as e:
            logger.error(f"❌ Create event error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def create_event(self, event_data: Dict) -> Dict[str, Any]:
        """
        🔗 PUBLIC API ZA KREIRANJE EVENTA (pozivaju ostali agenti)
        """
        try:
            # Convert event_data to proper format
            intent = {
                'event_title': event_data.get('title', 'Event from Agent'),
                'date': event_data.get('date', 'today'),
                'time': event_data.get('time', '09:00'),
                'duration': 60,  # default 1h
                'event_type': 'meeting',
                'participants': event_data.get('participants', [])
            }
            
            return await self._create_event(intent, {'user_id': 'agent_system'})
            
        except Exception as e:
            logger.error(f"❌ Agent create event error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _daily_overview(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📋 DAILY CALENDAR OVERVIEW
        """
        try:
            today = date.today()
            events_today = self._get_events_for_date(today)
            
            # Upcoming events (next 3 days)
            upcoming_events = []
            for i in range(1, 4):
                future_date = today + timedelta(days=i)
                future_events = self._get_events_for_date(future_date)
                for event in future_events:
                    event['days_ahead'] = i
                    upcoming_events.append(event)
            
            # Today's stats
            total_duration = sum(e.get('duration_minutes', 60) for e in events_today)
            busy_hours = total_duration // 60
            busy_minutes = total_duration % 60
            
            # Reminders due today
            due_reminders = self._get_due_reminders(today)
            
            return {
                'success': True,
                'date': today.isoformat(),
                'today_events': events_today,
                'upcoming_events': upcoming_events[:10],  # Top 10
                'stats': {
                    'total_events_today': len(events_today),
                    'total_busy_time': f"{busy_hours}h {busy_minutes}m",
                    'first_event': events_today[0]['time'] if events_today else None,
                    'last_event': events_today[-1]['time'] if events_today else None
                },
                'due_reminders': due_reminders,
                'weather_note': '☀️ Perfect day for meetings!',  # Mock weather
                'daily_tip': self._get_daily_productivity_tip(),
                'actions': [
                    'Add new event',
                    'Reschedule events', 
                    'Set additional reminders',
                    'View weekly overview'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Daily overview error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _get_reminders(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ⏰ GET ACTIVE REMINDERS
        """
        try:
            now = datetime.now()
            active_reminders = []
            
            # Check all events for due reminders
            for date_key, events in self.events_storage.items():
                event_date = datetime.fromisoformat(date_key)
                for event in events:
                    event_datetime = datetime.combine(
                        event_date.date(), 
                        datetime.strptime(event['time'], '%H:%M').time()
                    )
                    
                    # Calculate reminder time
                    reminder_time = event_datetime - timedelta(minutes=event['reminder_before'])
                    
                    # Check if reminder is due (within next hour)
                    if reminder_time <= now + timedelta(hours=1) and event_datetime > now:
                        active_reminders.append({
                            'event_id': event['id'],
                            'event_title': event['title'],
                            'event_time': event_datetime.isoformat(),
                            'reminder_time': reminder_time.isoformat(),
                            'minutes_until_event': int((event_datetime - now).total_seconds() // 60),
                            'icon': event['icon'],
                            'type': event['type']
                        })
            
            # Sort by reminder time
            active_reminders.sort(key=lambda x: x['reminder_time'])
            
            return {
                'success': True,
                'active_reminders': active_reminders,
                'total_reminders': len(active_reminders),
                'next_reminder': active_reminders[0] if active_reminders else None,
                'notification_settings': {
                    'desktop_notifications': True,
                    'email_reminders': True,
                    'viber_reminders': True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Get reminders error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _parse_date(self, date_string: str) -> date:
        """
        🗓️ PARSE DATE STRING TO DATE OBJECT
        """
        if not date_string or date_string == 'today' or date_string == 'danas':
            return date.today()
        elif date_string == 'tomorrow' or date_string == 'sutra':
            return date.today() + timedelta(days=1)
        elif date_string == 'day after tomorrow' or date_string == 'preksutra':
            return date.today() + timedelta(days=2)
        else:
            # Try to parse specific date formats
            try:
                # Try DD.MM.YYYY
                if '.' in date_string:
                    parts = date_string.split('.')
                    return date(int(parts[2]), int(parts[1]), int(parts[0]))
                # Try YYYY-MM-DD
                elif '-' in date_string:
                    return datetime.fromisoformat(date_string).date()
                else:
                    return date.today()  # Fallback
            except:
                return date.today()  # Fallback
    
    def _get_events_for_date(self, target_date: date) -> List[Dict]:
        """
        📅 GET ALL EVENTS FOR SPECIFIC DATE
        """
        date_key = target_date.isoformat()
        events = self.events_storage.get(date_key, [])
        
        # Sort by time
        return sorted(events, key=lambda x: x['time'])
    
    def _check_conflicts(self, new_event: Dict, event_date: date) -> List[Dict]:
        """
        ⚠️ CHECK FOR TIME CONFLICTS
        """
        existing_events = self._get_events_for_date(event_date)
        conflicts = []
        
        new_start = datetime.strptime(new_event['time'], '%H:%M').time()
        new_end = (datetime.combine(event_date, new_start) + 
                   timedelta(minutes=new_event['duration_minutes'])).time()
        
        for event in existing_events:
            event_start = datetime.strptime(event['time'], '%H:%M').time()
            event_end = (datetime.combine(event_date, event_start) + 
                        timedelta(minutes=event.get('duration_minutes', 60))).time()
            
            # Check overlap
            if not (new_end <= event_start or new_start >= event_end):
                conflicts.append({
                    'conflicting_event': event,
                    'overlap_type': 'partial' if (new_start < event_start or new_end > event_end) else 'full'
                })
        
        return conflicts
    
    def _calculate_busy_hours(self, events: List[Dict]) -> float:
        """
        ⏱️ CALCULATE TOTAL BUSY HOURS
        """
        total_minutes = sum(e.get('duration_minutes', 60) for e in events)
        return round(total_minutes / 60.0, 1)
    
    def _find_free_slots(self, target_date: date, events: List[Dict]) -> List[Dict]:
        """
        🆓 FIND FREE TIME SLOTS
        """
        # Define work hours (9:00 - 18:00)
        work_start = datetime.strptime('09:00', '%H:%M').time()
        work_end = datetime.strptime('18:00', '%H:%M').time()
        
        # Create busy periods
        busy_periods = []
        for event in events:
            event_start = datetime.strptime(event['time'], '%H:%M').time()
            event_end = (datetime.combine(target_date, event_start) + 
                        timedelta(minutes=event.get('duration_minutes', 60))).time()
            busy_periods.append((event_start, event_end))
        
        # Sort busy periods
        busy_periods.sort()
        
        # Find free slots
        free_slots = []
        current_time = work_start
        
        for start, end in busy_periods:
            if current_time < start:
                free_slots.append({
                    'start_time': current_time.strftime('%H:%M'),
                    'end_time': start.strftime('%H:%M'),
                    'duration_minutes': int((datetime.combine(target_date, start) - 
                                          datetime.combine(target_date, current_time)).total_seconds() // 60)
                })
            current_time = max(current_time, end)
        
        # Add final free slot if any
        if current_time < work_end:
            free_slots.append({
                'start_time': current_time.strftime('%H:%M'),
                'end_time': work_end.strftime('%H:%M'),
                'duration_minutes': int((datetime.combine(target_date, work_end) - 
                                      datetime.combine(target_date, current_time)).total_seconds() // 60)
            })
        
        return [slot for slot in free_slots if slot['duration_minutes'] >= 30]  # Min 30min slots
    
    def _get_due_reminders(self, target_date: date) -> List[Dict]:
        """
        🔔 GET REMINDERS DUE TODAY
        """
        # Mock implementation
        return [
            {
                'type': 'daily_standup',
                'message': 'Daily team standup in 30 minutes',
                'time': '09:30'
            },
            {
                'type': 'client_call',
                'message': 'Important client call at 14:00',
                'time': '13:45'
            }
        ]
    
    def _get_daily_productivity_tip(self) -> str:
        """
        💡 RANDOM DAILY PRODUCTIVITY TIP
        """
        tips = [
            "💡 Planiraj najvažnije zadatke ujutru kada si najsvežiji!",
            "⚡ Koristi Pomodoro tehniku: 25min rada + 5min pauza",
            "📝 Pripremi agenda za sve meeting-e unapred",
            "🎯 Fokusiraj se na 3 najvažnije stvari danas",
            "☕ Uzmi kratku pauzu svaka 2 sata za bolju koncentraciju"
        ]
        import random
        return random.choice(tips)
    
    async def _general_calendar_help(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ❓ GENERAL CALENDAR HELP
        """
        return {
            'success': True,
            'message': "Calendar Agent ready! 📅",
            'available_actions': [
                'View daily calendar',
                'Create events and meetings',
                'Set reminders',
                'Check for conflicts',
                'Get productivity insights'
            ],
            'examples': [
                "Show today's calendar",
                "Create meeting tomorrow at 14:00",
                "Set reminder for project deadline",
                "Check free slots next week"
            ],
            'event_types': list(self.event_types.keys())
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        🩺 CALENDAR AGENT HEALTH CHECK
        """
        total_events = sum(len(events) for events in self.events_storage.values())
        
        return {
            'status': 'healthy',
            'total_events_stored': total_events,
            'event_types_supported': len(self.event_types),
            'capabilities_active': len(self.capabilities),
            'last_check': datetime.now().isoformat()
        }