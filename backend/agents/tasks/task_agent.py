"""
✅ TASK AGENT - BRUTALNI TASK MANAGEMENT ✅
- Task kreiranje i upravljanje
- Priority sistem
- Deadline tracking
- Project organizacija
- Progress monitoring
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, date
import logging
import json
import uuid

logger = logging.getLogger(__name__)

class TaskAgent:
    """
    ✅ BRUTALNI TASK AGENT ✅
    Complete task management solution
    """
    
    def __init__(self):
        self.description = "Advanced Task & Project Management Agent"
        self.capabilities = [
            "Create and manage tasks",
            "Priority-based task sorting",
            "Deadline tracking",
            "Project organization", 
            "Progress monitoring",
            "Subtask breakdown",
            "Time estimation",
            "Dependency management"
        ]
        
        # Task storage
        self.tasks_storage = {}
        self.projects_storage = {}
        
        # Priority levels
        self.priority_levels = {
            'critical': {'value': 5, 'icon': '🔥', 'color': 'red'},
            'high': {'value': 4, 'icon': '⚡', 'color': 'orange'},
            'medium': {'value': 3, 'icon': '📋', 'color': 'blue'},
            'low': {'value': 2, 'icon': '📝', 'color': 'green'},
            'someday': {'value': 1, 'icon': '💭', 'color': 'gray'}
        }
        
        # Task status
        self.task_statuses = {
            'todo': {'icon': '⏳', 'color': 'blue'},
            'in_progress': {'icon': '🔄', 'color': 'orange'},
            'waiting': {'icon': '⏸️', 'color': 'yellow'},
            'done': {'icon': '✅', 'color': 'green'},
            'cancelled': {'icon': '❌', 'color': 'red'}
        }
        
        logger.info("✅ Task Agent initialized!")
    
    async def execute(self, user_input: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎯 GLAVNA TASK EXECUTION FUNKCIJA
        """
        try:
            logger.info(f"✅ Processing task request: {user_input[:100]}...")
            
            # Parse user intent
            intent = self._parse_task_intent(user_input)
            
            if intent['action'] == 'create':
                return await self._create_task(intent, user_context)
            elif intent['action'] == 'list':
                return await self._list_tasks(intent, user_context)
            elif intent['action'] == 'update':
                return await self._update_task(intent, user_context)
            elif intent['action'] == 'complete':
                return await self._complete_task(intent, user_context)
            elif intent['action'] == 'project':
                return await self._manage_project(intent, user_context)
            else:
                return await self._general_task_help(intent, user_context)
                
        except Exception as e:
            logger.error(f"❌ Task agent error: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': ['Check task details', 'Verify project name', 'Try simpler command']
            }
    
    def _parse_task_intent(self, user_input: str) -> Dict[str, Any]:
        """
        🔍 PARSES TASK INTENT FROM USER INPUT
        """
        input_lower = user_input.lower()
        
        intent = {
            'action': 'list',
            'task_title': None,
            'priority': 'medium',
            'deadline': None,
            'project': None,
            'tags': [],
            'assignee': None
        }
        
        # Detect action
        if any(word in input_lower for word in ['create', 'add', 'new', 'napravi', 'dodaj', 'novi']):
            intent['action'] = 'create'
        elif any(word in input_lower for word in ['complete', 'done', 'finish', 'završi', 'gotovo']):
            intent['action'] = 'complete'
        elif any(word in input_lower for word in ['update', 'edit', 'change', 'promeni', 'izmeni']):
            intent['action'] = 'update'
        elif any(word in input_lower for word in ['project', 'projekat']):
            intent['action'] = 'project'
        elif any(word in input_lower for word in ['list', 'show', 'view', 'prikaži', 'lista']):
            intent['action'] = 'list'
        
        # Detect priority
        if any(word in input_lower for word in ['critical', 'urgent', 'kritično', 'hitno']):
            intent['priority'] = 'critical'
        elif any(word in input_lower for word in ['high', 'important', 'važno', 'visok']):
            intent['priority'] = 'high'
        elif any(word in input_lower for word in ['low', 'nizak', 'kasnije']):
            intent['priority'] = 'low'
        elif any(word in input_lower for word in ['someday', 'možda', 'nekad']):
            intent['priority'] = 'someday'
        
        # Extract task title (simple heuristic)
        if intent['action'] == 'create':
            # Find text after create/add keywords
            for keyword in ['create', 'add', 'new', 'napravi', 'dodaj', 'novi']:
                if keyword in input_lower:
                    parts = user_input.split(keyword, 1)
                    if len(parts) > 1:
                        title_part = parts[1].strip()
                        # Clean up common words
                        title_part = title_part.replace('task', '').replace('zadatak', '').strip()
                        intent['task_title'] = title_part[:100] if title_part else 'New Task'
                    break
        
        return intent
    
    async def _create_task(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ➕ CREATE NEW TASK
        """
        try:
            task_id = str(uuid.uuid4())
            
            new_task = {
                'id': task_id,
                'title': intent.get('task_title', 'New Task'),
                'description': '',
                'priority': intent.get('priority', 'medium'),
                'status': 'todo',
                'created_at': datetime.now().isoformat(),
                'created_by': user_context.get('user_id', 'system'),
                'updated_at': datetime.now().isoformat(),
                'deadline': intent.get('deadline'),
                'project': intent.get('project'),
                'tags': intent.get('tags', []),
                'assignee': intent.get('assignee'),
                'estimated_hours': None,
                'actual_hours': 0,
                'progress_percentage': 0,
                'subtasks': [],
                'dependencies': [],
                'notes': []
            }
            
            # Store task
            self.tasks_storage[task_id] = new_task
            
            # Add to project if specified
            if new_task['project']:
                await self._add_task_to_project(task_id, new_task['project'])
            
            return {
                'success': True,
                'task_created': new_task,
                'message': f"Task '{new_task['title']}' created with {new_task['priority']} priority",
                'priority_info': self.priority_levels[new_task['priority']],
                'actions': [
                    'Set deadline',
                    'Add subtasks',
                    'Assign to project',
                    'Set time estimate'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Create task error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _list_tasks(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📋 LIST TASKS
        """
        try:
            all_tasks = list(self.tasks_storage.values())
            
            # Filter by status, priority, project etc.
            filtered_tasks = all_tasks
            
            # Sort by priority and created date
            filtered_tasks.sort(key=lambda t: (
                -self.priority_levels[t['priority']]['value'],
                t['created_at']
            ))
            
            # Group by status
            tasks_by_status = {}
            for task in filtered_tasks:
                status = task['status']
                if status not in tasks_by_status:
                    tasks_by_status[status] = []
                tasks_by_status[status].append(task)
            
            # Calculate stats
            total_tasks = len(all_tasks)
            completed_tasks = len([t for t in all_tasks if t['status'] == 'done'])
            overdue_tasks = self._get_overdue_tasks(all_tasks)
            
            return {
                'success': True,
                'tasks_by_status': tasks_by_status,
                'stats': {
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'completion_rate': round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0,
                    'overdue_tasks': len(overdue_tasks),
                    'in_progress_tasks': len([t for t in all_tasks if t['status'] == 'in_progress'])
                },
                'overdue_tasks': overdue_tasks,
                'actions': [
                    'Create new task',
                    'Update task status',
                    'Set priorities',
                    'Organize into projects'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ List tasks error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _complete_task(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ✅ COMPLETE TASK
        """
        try:
            # Find task by title or ID (simple implementation)
            task_title = intent.get('task_title', '').lower()
            completed_task = None
            
            for task_id, task in self.tasks_storage.items():
                if task_title in task['title'].lower():
                    task['status'] = 'done'
                    task['completed_at'] = datetime.now().isoformat()
                    task['updated_at'] = datetime.now().isoformat()
                    task['progress_percentage'] = 100
                    completed_task = task
                    break
            
            if not completed_task:
                return {
                    'success': False,
                    'error': 'Task not found',
                    'suggestion': 'Try listing tasks first to see available tasks'
                }
            
            return {
                'success': True,
                'completed_task': completed_task,
                'message': f"Task '{completed_task['title']}' marked as completed! 🎉",
                'celebration': '🎉🎊✨',
                'actions': [
                    'Archive task',
                    'Create follow-up task',
                    'Share completion',
                    'Update project progress'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Complete task error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _manage_project(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        📁 MANAGE PROJECT
        """
        try:
            project_name = intent.get('project', 'Default Project')
            
            if project_name not in self.projects_storage:
                # Create new project
                self.projects_storage[project_name] = {
                    'name': project_name,
                    'created_at': datetime.now().isoformat(),
                    'tasks': [],
                    'description': '',
                    'status': 'active'
                }
            
            project = self.projects_storage[project_name]
            
            # Get project tasks
            project_tasks = [
                task for task in self.tasks_storage.values() 
                if task.get('project') == project_name
            ]
            
            # Calculate project stats
            total_tasks = len(project_tasks)
            completed_tasks = len([t for t in project_tasks if t['status'] == 'done'])
            progress = round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0
            
            return {
                'success': True,
                'project': project,
                'project_tasks': project_tasks,
                'stats': {
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'progress_percentage': progress,
                    'active_tasks': len([t for t in project_tasks if t['status'] in ['todo', 'in_progress']])
                },
                'actions': [
                    'Add tasks to project',
                    'Set project deadline',
                    'Assign team members',
                    'Generate project report'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Manage project error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_overdue_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        ⏰ GET OVERDUE TASKS
        """
        now = datetime.now()
        overdue = []
        
        for task in tasks:
            if task['deadline'] and task['status'] != 'done':
                try:
                    deadline = datetime.fromisoformat(task['deadline'])
                    if deadline < now:
                        task['days_overdue'] = (now - deadline).days
                        overdue.append(task)
                except:
                    continue
        
        return overdue
    
    async def _add_task_to_project(self, task_id: str, project_name: str):
        """
        📁 ADD TASK TO PROJECT
        """
        if project_name not in self.projects_storage:
            self.projects_storage[project_name] = {
                'name': project_name,
                'created_at': datetime.now().isoformat(),
                'tasks': [],
                'description': '',
                'status': 'active'
            }
        
        if task_id not in self.projects_storage[project_name]['tasks']:
            self.projects_storage[project_name]['tasks'].append(task_id)
    
    async def _general_task_help(self, intent: Dict, user_context: Dict) -> Dict[str, Any]:
        """
        ❓ GENERAL TASK HELP
        """
        return {
            'success': True,
            'message': "Task Agent ready for action! ✅",
            'available_actions': [
                'Create new tasks',
                'List and organize tasks',
                'Set priorities and deadlines',
                'Manage projects',
                'Track progress',
                'Generate reports'
            ],
            'examples': [
                "Create high priority task: Fix bug in login",
                "List all my tasks",
                "Complete task: Prepare presentation", 
                "Show project progress"
            ],
            'priority_levels': list(self.priority_levels.keys()),
            'task_statuses': list(self.task_statuses.keys())
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        🩺 TASK AGENT HEALTH CHECK
        """
        total_tasks = len(self.tasks_storage)
        total_projects = len(self.projects_storage)
        
        return {
            'status': 'healthy',
            'total_tasks': total_tasks,
            'total_projects': total_projects,
            'priority_levels': len(self.priority_levels),
            'capabilities_active': len(self.capabilities),
            'last_check': datetime.now().isoformat()
        }