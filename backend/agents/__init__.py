"""
🤖 AGENTS MODULE INIT 🤖
Brutalni Agent System za MasterCoderAI
"""

from .core.agent_dispatcher import dispatcher
from .agents_api import router

__all__ = ['dispatcher', 'router']