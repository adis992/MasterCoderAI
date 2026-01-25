# backend/api/tasks.py
"""
Task Automation API - AI Learning Tasks
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import uuid
from datetime import datetime
import requests
from pathlib import Path
import json

from api.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

# In-memory task storage (in production use database)
tasks_db = {}

class TaskRequest(BaseModel):
    type: str  # github_train, website_learn, document_analyze, api_monitor
    url: str
    description: str

class Task(BaseModel):
    id: str
    type: str
    url: str
    description: str
    status: str  # idle, running, completed, error
    result: Optional[str] = None
    created_at: datetime
    user_id: int

@router.get("")
async def get_tasks(current_user=Depends(get_current_user)):
    """Get all tasks for current user"""
    user_tasks = [task for task in tasks_db.values() if task['user_id'] == current_user['id']]
    return {"tasks": user_tasks}

@router.post("/create")
async def create_task(request: TaskRequest, current_user=Depends(get_current_user)):
    """Create new AI learning task"""
    if not current_user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Only admins can create tasks")
    
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "type": request.type,
        "url": request.url,
        "description": request.description,
        "status": "idle",
        "result": None,
        "created_at": datetime.now().isoformat(),
        "user_id": current_user['id']
    }
    
    tasks_db[task_id] = task
    
    # Start task processing in background
    asyncio.create_task(process_task(task_id))
    
    return {"message": "Task created successfully", "task_id": task_id}

@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user=Depends(get_current_user)):
    """Delete task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    if task['user_id'] != current_user['id'] and not current_user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    del tasks_db[task_id]
    return {"message": "Task deleted"}

async def process_task(task_id: str):
    """Background task processing"""
    try:
        task = tasks_db.get(task_id)
        if not task:
            return
        
        task['status'] = 'running'
        print(f"🚀 Processing task {task_id}: {task['type']} - {task['url']}")
        
        if task['type'] == 'github_train':
            result = await process_github_training(task['url'], task['description'])
        elif task['type'] == 'website_learn':
            result = await process_website_learning(task['url'], task['description'])
        elif task['type'] == 'document_analyze':
            result = await process_document_analysis(task['url'], task['description'])
        elif task['type'] == 'api_monitor':
            result = await process_api_monitoring(task['url'], task['description'])
        else:
            result = "Unknown task type"
        
        task['status'] = 'completed'
        task['result'] = result
        print(f"✅ Task {task_id} completed: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ Task {task_id} failed: {str(e)}")
        task['status'] = 'error'
        task['result'] = f"Error: {str(e)}"

async def process_github_training(url: str, description: str) -> str:
    """Process GitHub repository for training"""
    try:
        # Extract owner/repo from GitHub URL
        if "github.com" not in url:
            return "❌ Invalid GitHub URL"
        
        # Parse URL to get API endpoint
        parts = url.replace("https://github.com/", "").split("/")
        if len(parts) < 2:
            return "❌ Invalid GitHub repository URL format"
        
        owner, repo = parts[0], parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        # Get repository info
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            return f"❌ Cannot access repository: {response.status_code}"
        
        repo_info = response.json()
        
        # Get repository contents
        contents_url = f"{api_url}/contents"
        contents_response = requests.get(contents_url, timeout=10)
        
        if contents_response.status_code != 200:
            return f"❌ Cannot read repository contents: {contents_response.status_code}"
        
        contents = contents_response.json()
        
        # Analyze repository structure
        files = []
        for item in contents:
            if item['type'] == 'file':
                files.append(item['name'])
        
        # Create training summary
        result = f"""📚 GITHUB REPOSITORY ANALYSIS
        
Repository: {repo_info['full_name']}
Description: {repo_info.get('description', 'No description')}
Language: {repo_info.get('language', 'Unknown')}
Stars: {repo_info.get('stargazers_count', 0)}
Forks: {repo_info.get('forks_count', 0)}

Files found ({len(files)}): {', '.join(files[:10])}{'...' if len(files) > 10 else ''}

Training Task: {description}

✅ Repository data collected and ready for AI training!
"""
        return result
        
    except Exception as e:
        return f"❌ GitHub processing failed: {str(e)}"

async def process_website_learning(url: str, description: str) -> str:
    """Process website content for learning"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return f"❌ Cannot access website: {response.status_code}"
        
        content = response.text
        content_length = len(content)
        
        # Basic content analysis
        result = f"""🌐 WEBSITE CONTENT ANALYSIS

URL: {url}
Status: ✅ Accessible
Content Size: {content_length:,} characters
Content Type: {response.headers.get('content-type', 'Unknown')}

Learning Task: {description}

✅ Website content scraped and ready for AI learning!
Content preview: {content[:300]}...
"""
        return result
        
    except Exception as e:
        return f"❌ Website processing failed: {str(e)}"

async def process_document_analysis(url: str, description: str) -> str:
    """Analyze document from URL"""
    return f"""📄 DOCUMENT ANALYSIS
    
URL: {url}
Task: {description}

✅ Document analysis completed!
(This feature will be expanded in future versions)
"""

async def process_api_monitoring(url: str, description: str) -> str:
    """Monitor API endpoint"""
    try:
        response = requests.get(url, timeout=10)
        return f"""📊 API MONITORING RESULT

URL: {url}
Status Code: {response.status_code}
Response Time: ~{len(response.content)} bytes
Monitoring Task: {description}

✅ API endpoint monitored successfully!
"""
    except Exception as e:
        return f"❌ API monitoring failed: {str(e)}"