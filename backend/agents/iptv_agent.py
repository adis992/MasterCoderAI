"""
📺 IPTV AGENT - Xtream UI Panel Integration
Handles IPTV user management and support
"""
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class IPTVAgent:
    """Agent for Xtream UI Panel integration"""
    
    def __init__(self, panel_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.panel_url = panel_url
        self.username = username
        self.password = password
        
    def set_credentials(self, panel_url: str, username: str, password: str):
        """Update Xtream UI credentials"""
        self.panel_url = panel_url
        self.username = username
        self.password = password
        
    def verify_connection(self) -> Dict:
        """Verify Xtream UI Panel connection"""
        if not all([self.panel_url, self.username, self.password]):
            return {
                "status": "error",
                "message": "Xtream UI credentials not configured"
            }
        
        try:
            # Test authentication
            url = f"{self.panel_url}/player_api.php"
            params = {
                "username": self.username,
                "password": self.password
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "user_info" in data:
                    return {
                        "status": "ok",
                        "message": "Xtream UI connected successfully",
                        "user_info": {
                            "username": data["user_info"].get("username"),
                            "status": data["user_info"].get("status"),
                            "exp_date": data["user_info"].get("exp_date")
                        }
                    }
            
            return {
                "status": "error",
                "message": "Invalid credentials or panel URL"
            }
        except Exception as e:
            logger.error(f"Xtream UI verification error: {str(e)}")
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}"
            }
    
    def get_users(self) -> List[Dict]:
        """Get list of IPTV users (requires admin API)"""
        # This requires admin panel API access
        # Placeholder implementation
        return []
    
    def get_user_info(self, username: str) -> Dict:
        """Get specific user information"""
        if not all([self.panel_url, self.username, self.password]):
            return {
                "status": "error",
                "message": "Credentials not configured"
            }
        
        try:
            url = f"{self.panel_url}/player_api.php"
            params = {
                "username": username,
                "password": self.password  # Admin password
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "ok",
                    "user_info": data.get("user_info", {}),
                    "server_info": data.get("server_info", {})
                }
            
            return {
                "status": "error",
                "message": f"HTTP error: {response.status_code}"
            }
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_live_streams(self) -> List[Dict]:
        """Get available live streams"""
        if not all([self.panel_url, self.username, self.password]):
            return []
        
        try:
            url = f"{self.panel_url}/player_api.php"
            params = {
                "username": self.username,
                "password": self.password,
                "action": "get_live_streams"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            
            return []
        except Exception as e:
            logger.error(f"Get streams error: {str(e)}")
            return []

# Global instance
_iptv_agent = None

def get_iptv_agent(panel_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None) -> IPTVAgent:
    """Get or create IPTV agent instance"""
    global _iptv_agent
    if _iptv_agent is None:
        _iptv_agent = IPTVAgent(panel_url, username, password)
    elif panel_url and username and password:
        _iptv_agent.set_credentials(panel_url, username, password)
    return _iptv_agent
