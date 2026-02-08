"""
🟣 VIBER AGENT - Viber messaging integration
Handles Viber API communication for IPTV support
"""
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ViberAgent:
    """Agent for Viber messaging integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VIBER_API_KEY")
        self.base_url = "https://chatapi.viber.com/pa"
        self.bot_name = os.getenv("VIBER_BOT_NAME", "IPTV Support Bot")
        
    def set_api_key(self, api_key: str):
        """Update Viber API key"""
        self.api_key = api_key
        
    def verify_connection(self) -> Dict:
        """Verify Viber API connection"""
        if not self.api_key:
            return {
                "status": "error",
                "message": "Viber API key not configured"
            }
        
        try:
            headers = {
                "X-Viber-Auth-Token": self.api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.base_url}/get_account_info",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "ok",
                    "message": "Viber API connected successfully",
                    "bot_info": {
                        "name": data.get("name", "Unknown"),
                        "uri": data.get("uri", ""),
                        "webhook": data.get("webhook", "")
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Viber API error: {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Viber verification error: {str(e)}")
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}"
            }
    
    def get_messages(self, limit: int = 50) -> List[Dict]:
        """Get recent Viber messages (requires webhook setup)"""
        # Note: Viber doesn't provide a pull API for messages
        # Messages are received via webhooks
        # This is a placeholder for the webhook-received messages
        return []
    
    def send_message(self, receiver_id: str, message: str, sender_name: str = None) -> Dict:
        """Send message via Viber"""
        if not self.api_key:
            return {
                "status": "error",
                "message": "Viber API key not configured"
            }
        
        try:
            headers = {
                "X-Viber-Auth-Token": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "receiver": receiver_id,
                "type": "text",
                "text": message,
                "sender": {
                    "name": sender_name or self.bot_name
                }
            }
            
            response = requests.post(
                f"{self.base_url}/send_message",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 0:
                    return {
                        "status": "ok",
                        "message": "Message sent successfully",
                        "message_token": data.get("message_token")
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Viber error: {data.get('status_message', 'Unknown error')}"
                    }
            else:
                return {
                    "status": "error",
                    "message": f"HTTP error: {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Viber send error: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to send: {str(e)}"
            }
    
    def set_webhook(self, webhook_url: str) -> Dict:
        """Set Viber webhook URL"""
        if not self.api_key:
            return {
                "status": "error",
                "message": "Viber API key not configured"
            }
        
        try:
            headers = {
                "X-Viber-Auth-Token": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "url": webhook_url,
                "event_types": [
                    "delivered",
                    "seen",
                    "failed",
                    "subscribed",
                    "unsubscribed",
                    "conversation_started"
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/set_webhook",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 0:
                    return {
                        "status": "ok",
                        "message": "Webhook set successfully",
                        "event_types": data.get("event_types", [])
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Viber error: {data.get('status_message', 'Unknown error')}"
                    }
            else:
                return {
                    "status": "error",
                    "message": f"HTTP error: {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Viber webhook error: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to set webhook: {str(e)}"
            }

# Global instance
_viber_agent = None

def get_viber_agent(api_key: Optional[str] = None) -> ViberAgent:
    """Get or create Viber agent instance"""
    global _viber_agent
    if _viber_agent is None:
        _viber_agent = ViberAgent(api_key)
    elif api_key:
        _viber_agent.set_api_key(api_key)
    return _viber_agent
