"""
AI module: AI integration and model management
"""

from .providers import AIProvider, OllamaProvider, AIMessage
from .ai_service import AIService

__all__ = ["AIProvider", "OllamaProvider", "AIMessage", "AIService"]
