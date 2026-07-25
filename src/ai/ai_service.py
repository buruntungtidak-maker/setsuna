"""
AI Service: High-level AI service for character interaction
"""

import logging
import asyncio
from typing import Optional
from .providers import AIProvider, OllamaProvider, AIMessage


class AIService:
    """
    AI Service for managing character conversations.
    
    Handles message processing, personality, and provider management.
    """
    
    def __init__(self, provider: Optional[AIProvider] = None):
        """
        Initialize AI Service.
        
        Args:
            provider: AI provider instance (default: OllamaProvider)
        """
        self.logger = logging.getLogger("AIService")
        self.provider = provider or OllamaProvider()
        self.conversation_history: list[AIMessage] = []
        
        self.system_prompt = """
You are Setsuna, a friendly and cute anime-style AI desktop companion.

Personality traits:
- Friendly and helpful
- Cute and playful
- Smart and knowledgeable
- Polite and respectful
- Easy to talk to
- Can understand emotions in conversations

When the user expresses emotions or asks for help, respond accordingly:
- If user is happy: match their energy, be cheerful
- If user is sad: be empathetic and supportive
- If user is angry: be calm and understanding
- If user asks for help: provide clear, concise assistance

Keep responses concise (1-3 sentences) unless more detail is needed.
Be warm and genuine in your responses.
"""
    
    def initialize(self) -> bool:
        """
        Initialize AI service.
        
        Returns:
            True if initialization successful, False otherwise
        """
        self.logger.info("Initializing AI Service...")
        if self.provider.initialize():
            self.logger.info("AI Service ready")
            return True
        else:
            self.logger.error("Failed to initialize AI provider")
            return False
    
    def is_ready(self) -> bool:
        """
        Check if AI service is ready.
        
        Returns:
            True if ready, False otherwise
        """
        return self.provider.is_available()
    
    async def chat(self, message: str) -> str:
        """
        Send message and get AI response.
        
        Args:
            message: User message
        
        Returns:
            AI response
        """
        try:
            # Add user message to history
            self.conversation_history.append(
                AIMessage(role="user", content=message)
            )
            
            # Get AI response
            response = await self.provider.chat(
                message,
                history=self.conversation_history[:-1],  # Exclude current message
                system_prompt=self.system_prompt
            )
            
            # Add AI response to history
            self.conversation_history.append(
                AIMessage(role="assistant", content=response)
            )
            
            # Keep history limited (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return response
            
        except Exception as e:
            self.logger.error(f"Chat error: {e}", exc_info=True)
            return "Sorry, I encountered an error. Please try again."
    
    def clear_history(self) -> None:
        """
        Clear conversation history.
        """
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
    
    def set_personality(self, personality: str) -> None:
        """
        Set custom personality prompt.
        
        Args:
            personality: Custom system prompt
        """
        self.system_prompt = personality
        self.logger.info("Personality updated")
    
    def get_history(self) -> list[AIMessage]:
        """
        Get conversation history.
        
        Returns:
            List of messages
        """
        return self.conversation_history.copy()
