"""
🟣 VIBER & IPTV API ENDPOINTS
Integration with Viber messaging and Xtream UI Panel
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import sqlite3
import logging

from ..db.database import get_db
from ..dependencies import get_current_user
from ..agents.viber_agent import get_viber_agent
from ..agents.iptv_agent import get_iptv_agent

router = APIRouter(prefix="/integrations", tags=["integrations"])
logger = logging.getLogger(__name__)

# ==================== MODELS ====================

class ViberConfig(BaseModel):
    api_key: str
    bot_name: Optional[str] = "IPTV Support Bot"
    webhook_url: Optional[str] = None

class ViberMessage(BaseModel):
    receiver_id: str
    message: str
    sender_name: Optional[str] = None

class IPTVConfig(BaseModel):
    panel_url: str
    username: str
    password: str

class ViberWebhook(BaseModel):
    event: str
    timestamp: int
    message_token: Optional[int] = None
    sender: Optional[Dict] = None
    message: Optional[Dict] = None

# ==================== VIBER ENDPOINTS ====================

@router.post("/viber/configure")
async def configure_viber(
    config: ViberConfig,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Configure Viber API integration"""
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    
    try:
        # Save to database
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS integrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL UNIQUE,
                config TEXT NOT NULL,
                enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        import json
        config_json = json.dumps({
            "api_key": config.api_key,
            "bot_name": config.bot_name,
            "webhook_url": config.webhook_url
        })
        
        cursor.execute("""
            INSERT OR REPLACE INTO integrations (service, config, enabled)
            VALUES (?, ?, 1)
        """, ("viber", config_json))
        
        db.commit()
        
        # Test connection
        agent = get_viber_agent(config.api_key)
        verify_result = agent.verify_connection()
        
        # Set webhook if provided
        if config.webhook_url:
            webhook_result = agent.set_webhook(config.webhook_url)
            verify_result["webhook"] = webhook_result
        
        return {
            "status": "ok",
            "message": "Viber configured successfully",
            "verification": verify_result
        }
    except Exception as e:
        logger.error(f"Viber config error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/viber/status")
async def viber_status(current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get Viber integration status"""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT config, enabled FROM integrations WHERE service = 'viber'")
        row = cursor.fetchone()
        
        if not row:
            return {
                "status": "not_configured",
                "enabled": False
            }
        
        import json
        config = json.loads(row[0])
        enabled = bool(row[1])
        
        if not enabled:
            return {
                "status": "disabled",
                "enabled": False
            }
        
        # Verify connection
        agent = get_viber_agent(config.get("api_key"))
        verify_result = agent.verify_connection()
        
        return {
            "status": "configured",
            "enabled": True,
            "bot_name": config.get("bot_name"),
            "webhook_url": config.get("webhook_url"),
            "connection": verify_result
        }
    except Exception as e:
        logger.error(f"Viber status error: {str(e)}")
        return {
            "status": "error",
            "enabled": False,
            "message": str(e)
        }

@router.post("/viber/send")
async def send_viber_message(
    message: ViberMessage,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Send message via Viber"""
    try:
        # Get Viber config
        cursor = db.cursor()
        cursor.execute("SELECT config FROM integrations WHERE service = 'viber' AND enabled = 1")
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=400, detail="Viber not configured")
        
        import json
        config = json.loads(row[0])
        
        # Send message
        agent = get_viber_agent(config.get("api_key"))
        result = agent.send_message(
            receiver_id=message.receiver_id,
            message=message.message,
            sender_name=message.sender_name or config.get("bot_name")
        )
        
        # Log message
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viber_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receiver_id TEXT NOT NULL,
                message TEXT NOT NULL,
                sender_name TEXT,
                status TEXT,
                sent_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO viber_messages (receiver_id, message, sender_name, status, sent_by)
            VALUES (?, ?, ?, ?, ?)
        """, (
            message.receiver_id,
            message.message,
            message.sender_name,
            result.get("status"),
            current_user.get("user_id")
        ))
        
        db.commit()
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Send Viber error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/viber/webhook")
async def viber_webhook(webhook: ViberWebhook):
    """Handle Viber webhook events"""
    try:
        # Log webhook event
        logger.info(f"Viber webhook event: {webhook.event}")
        
        # Handle different event types
        if webhook.event == "message":
            # Process incoming message
            sender = webhook.sender
            message = webhook.message
            
            # Here you can integrate with AI to auto-respond
            # For now, just log it
            logger.info(f"Message from {sender}: {message}")
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.get("/viber/messages")
async def get_viber_messages(
    limit: int = 50,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get Viber message history"""
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT 
                id, receiver_id, message, sender_name, status, created_at
            FROM viber_messages
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "id": row[0],
                "receiver_id": row[1],
                "message": row[2],
                "sender_name": row[3],
                "status": row[4],
                "created_at": row[5]
            })
        
        return messages
    except Exception as e:
        logger.error(f"Get messages error: {str(e)}")
        return []

# ==================== IPTV ENDPOINTS ====================

@router.post("/iptv/configure")
async def configure_iptv(
    config: IPTVConfig,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Configure Xtream UI Panel integration"""
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    
    try:
        import json
        config_json = json.dumps({
            "panel_url": config.panel_url,
            "username": config.username,
            "password": config.password
        })
        
        cursor = db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO integrations (service, config, enabled)
            VALUES (?, ?, 1)
        """, ("iptv", config_json))
        
        db.commit()
        
        # Test connection
        agent = get_iptv_agent(config.panel_url, config.username, config.password)
        verify_result = agent.verify_connection()
        
        return {
            "status": "ok",
            "message": "IPTV panel configured successfully",
            "verification": verify_result
        }
    except Exception as e:
        logger.error(f"IPTV config error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/iptv/status")
async def iptv_status(current_user = Depends(get_current_user), db = Depends(get_db)):
    """Get IPTV integration status"""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT config, enabled FROM integrations WHERE service = 'iptv'")
        row = cursor.fetchone()
        
        if not row:
            return {
                "status": "not_configured",
                "enabled": False
            }
        
        import json
        config = json.loads(row[0])
        enabled = bool(row[1])
        
        if not enabled:
            return {
                "status": "disabled",
                "enabled": False
            }
        
        # Verify connection
        agent = get_iptv_agent(
            config.get("panel_url"),
            config.get("username"),
            config.get("password")
        )
        verify_result = agent.verify_connection()
        
        return {
            "status": "configured",
            "enabled": True,
            "panel_url": config.get("panel_url"),
            "connection": verify_result
        }
    except Exception as e:
        logger.error(f"IPTV status error: {str(e)}")
        return {
            "status": "error",
            "enabled": False,
            "message": str(e)
        }

@router.get("/iptv/user/{username}")
async def get_iptv_user(
    username: str,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get IPTV user information"""
    try:
        # Get IPTV config
        cursor = db.cursor()
        cursor.execute("SELECT config FROM integrations WHERE service = 'iptv' AND enabled = 1")
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=400, detail="IPTV not configured")
        
        import json
        config = json.loads(row[0])
        
        # Get user info
        agent = get_iptv_agent(
            config.get("panel_url"),
            config.get("username"),
            config.get("password")
        )
        result = agent.get_user_info(username)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get IPTV user error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
