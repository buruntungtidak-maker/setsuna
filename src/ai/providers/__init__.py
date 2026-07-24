"""
AI Providers: Modular AI provider implementations
"""

from .base import AIProvider
from .ollama_provider import OllamaProvider

__all__ = ["AIProvider", "OllamaProvider"]
