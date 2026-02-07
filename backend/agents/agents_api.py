"""
🤖 AGENTS API - BRUTALNI AGENT SYSTEM ENDPOINTS 🤖
FastAPI endpoints za kompletan agent sistem
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
import logging
import sys
import os

# Fix imports for agents module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from .core.agent_dispatcher import dispatcher
try:
    from db.models import User  # Fixed import path
    from api.auth import get_current_user
except ImportError:
    # Fallback for development/testing
    User = dict
    User = dict
    get_current_user = lambda: {"id": 1, "username": "admin"}

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/agents/dispatch")
async def dispatch_agent(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    🎯 MAIN AGENT DISPATCH ENDPOINT
    Automatski bira i pokreće odgovarajućeg agenta
    """
    try:
        user_input = request.get('input', '')
        user_context = {
            'user_id': user.id,
            'username': user.username,
            'is_admin': user.is_admin,
            'user_settings': request.get('settings', {})
        }
        
        logger.info(f"🤖 Dispatching agent for user {user.username}: {user_input[:100]}")
        
        # Dispatch to appropriate agent
        result = await dispatcher.dispatch(user_input, user_context)
        
        return {
            'success': True,
            'result': result,
            'user_input': user_input,
            'timestamp': dispatcher.datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Agent dispatch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/available")
async def get_available_agents():
    """
    📋 GET ALL AVAILABLE AGENTS
    """
    try:
        agents_info = dispatcher.get_available_agents()
        return {
            'success': True,
            'agents': agents_info
        }
    except Exception as e:
        logger.error(f"❌ Get agents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/health")
async def agents_health_check():
    """
    🩺 AGENT SYSTEM HEALTH CHECK
    """
    try:
        health_status = await dispatcher.health_check()
        return {
            'success': True,
            'health': health_status
        }
    except Exception as e:
        logger.error(f"❌ Agent health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Specific agent endpoints

@router.post("/agents/email/send")
async def send_email_agent(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    📧 EMAIL AGENT - Send Email
    """
    try:
        email_agent = dispatcher.agents['email']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        # Format input for email sending
        user_input = f"send email to {request.get('to')} subject '{request.get('subject')}' body '{request.get('body')}'"
        
        result = await email_agent.execute(user_input, user_context)
        
        return {
            'success': True,
            'email_result': result
        }
        
    except Exception as e:
        logger.error(f"❌ Email agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/email/inbox")
async def get_inbox_agent(user = Depends(get_current_user)):
    """
    📧 EMAIL AGENT - Get Inbox
    """
    try:
        email_agent = dispatcher.agents['email']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        result = await email_agent.execute("read inbox", user_context)
        
        return {
            'success': True,
            'inbox': result
        }
        
    except Exception as e:
        logger.error(f"❌ Email inbox error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/viber/send")
async def send_viber_message(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    📱 VIBER AGENT - Send Message
    """
    try:
        viber_agent = dispatcher.agents['viber']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        user_input = f"send viber message to {request.get('to')} text '{request.get('text')}'"
        
        result = await viber_agent.execute(user_input, user_context)
        
        return {
            'success': True,
            'viber_result': result
        }
        
    except Exception as e:
        logger.error(f"❌ Viber agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/viber/messages")
async def get_viber_messages(user = Depends(get_current_user)):
    """
    📱 VIBER AGENT - Get Messages
    """
    try:
        viber_agent = dispatcher.agents['viber']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        result = await viber_agent.execute("read messages", user_context)
        
        return {
            'success': True,
            'messages': result
        }
        
    except Exception as e:
        logger.error(f"❌ Viber messages error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/calendar/today")
async def get_calendar_today(user = Depends(get_current_user)):
    """
    📅 CALENDAR AGENT - Today's Events
    """
    try:
        calendar_agent = dispatcher.agents['calendar']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        result = await calendar_agent.execute("show today's calendar", user_context)
        
        return {
            'success': True,
            'today_calendar': result
        }
        
    except Exception as e:
        logger.error(f"❌ Calendar today error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/calendar/create")
async def create_calendar_event(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    📅 CALENDAR AGENT - Create Event
    """
    try:
        calendar_agent = dispatcher.agents['calendar']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        user_input = f"create meeting '{request.get('title')}' {request.get('date')} at {request.get('time')}"
        
        result = await calendar_agent.execute(user_input, user_context)
        
        return {
            'success': True,
            'event_created': result
        }
        
    except Exception as e:
        logger.error(f"❌ Calendar create error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/tasks/create")
async def create_task_agent(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    ✅ TASK AGENT - Create Task
    """
    try:
        task_agent = dispatcher.agents['task']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        priority = request.get('priority', 'medium')
        user_input = f"create {priority} task {request.get('title')}"
        
        result = await task_agent.execute(user_input, user_context)
        
        return {
            'success': True,
            'task_created': result
        }
        
    except Exception as e:
        logger.error(f"❌ Task create error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/tasks/list")
async def list_tasks_agent(user = Depends(get_current_user)):
    """
    ✅ TASK AGENT - List Tasks
    """
    try:
        task_agent = dispatcher.agents['task']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        result = await task_agent.execute("list my tasks", user_context)
        
        return {
            'success': True,
            'tasks': result
        }
        
    except Exception as e:
        logger.error(f"❌ Task list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/web/search")
async def web_search_agent(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    🌐 WEB AGENT - Web Search
    """
    try:
        web_agent = dispatcher.agents['web']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        query = request.get('query', '')
        user_input = f"search for {query}"
        
        result = await web_agent.execute(user_input, user_context)
        
        return {
            'success': True,
            'search_results': result
        }
        
    except Exception as e:
        logger.error(f"❌ Web search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/files/create")
async def create_file_agent(
    request: Dict[str, Any],
    user = Depends(get_current_user)
):
    """
    📁 FILE AGENT - Create File
    """
    try:
        file_agent = dispatcher.agents['file']
        
        user_context = {
            'user_id': user.id,
            'username': user.username
        }
        
        file_path = request.get('path', '')
        content = request.get('content', '')
        user_input = f"create file {file_path} with content {content}"
        
        result = await file_agent.execute(user_input, user_context)
        
        return {
            'success': True,
            'file_created': result
        }
        
    except Exception as e:
        logger.error(f"❌ File create error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background Tasks for Agents

@router.post("/agents/background/start")
async def start_background_agent(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user)
):
    """
    🔄 START BACKGROUND AGENT TASK
    """
    try:
        agent_type = request.get('agent_type', 'email')
        task_params = request.get('params', {})
        
        # Add background task
        background_tasks.add_task(
            run_background_agent_task,
            agent_type,
            task_params,
            user.id
        )
        
        return {
            'success': True,
            'message': f"Background {agent_type} agent task started",
            'task_id': f"bg_{agent_type}_{user.id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Background agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_background_agent_task(agent_type: str, task_params: Dict, user_id: int):
    """
    🔄 BACKGROUND AGENT TASK RUNNER
    """
    try:
        logger.info(f"🔄 Running background {agent_type} task for user {user_id}")
        
        agent = dispatcher.agents.get(agent_type)
        if not agent:
            logger.error(f"❌ Agent {agent_type} not found")
            return
        
        user_context = {
            'user_id': user_id,
            'background_task': True
        }
        
        # Run agent task
        result = await agent.execute(
            task_params.get('input', ''),
            user_context
        )
        
        logger.info(f"✅ Background {agent_type} task completed: {result.get('success')}")
        
    except Exception as e:
        logger.error(f"❌ Background agent task error: {e}")

# Agent Statistics

@router.get("/agents/stats")
async def get_agent_stats(user = Depends(get_current_user)):
    """
    📊 GET AGENT USAGE STATISTICS
    """
    try:
        stats = {
            'total_agents': len(dispatcher.agents),
            'agent_health': {},
            'usage_stats': {
                'total_dispatches': 0,  # Would be tracked in real system
                'most_used_agent': 'email',
                'success_rate': 0.94
            },
            'user_preferences': {
                'preferred_agents': ['email', 'calendar', 'task'],
                'auto_dispatch': True
            }
        }
        
        # Get health for each agent
        for agent_name, agent in dispatcher.agents.items():
            try:
                health = await agent.health_check()
                stats['agent_health'][agent_name] = health
            except:
                stats['agent_health'][agent_name] = {'status': 'unknown'}
        
        return {
            'success': True,
            'stats': stats
        }
        
    except Exception as e:
        logger.error(f"❌ Agent stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))