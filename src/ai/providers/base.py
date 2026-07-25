"""
Base AI Provider: Abstract base class for AI providers
"""

from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass


@dataclass
class AIMessage:
    """Represents an AI message"""
    role: str  # "user" or "assistant"
    content: str


class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    
    Defines interface for different AI backends (OpenAI, Ollama, LM Studio, etc.)
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the AI provider.
        
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def chat(
        self,
        message: str,
        history: Optional[list[AIMessage]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Send a chat message and get response.
        
        Args:
            message: User message
            history: Conversation history
            system_prompt: System prompt/personality
        
        Returns:
            AI response as string
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available/connected.
        
        Returns:
            True if available, False otherwise
        """
        pass
