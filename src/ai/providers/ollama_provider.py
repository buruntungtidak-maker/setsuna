"""
Ollama AI Provider: Integration with local Ollama models
"""

import logging
import httpx
from typing import Optional
from .base import AIProvider, AIMessage


class OllamaProvider(AIProvider):
    """
    Ollama AI Provider.
    
    Connects to local Ollama instance for LLM inference.
    Supports models like llama2, mistral, neural-chat, etc.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral",
        timeout: int = 120
    ):
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Ollama server URL
            model: Model name (default: mistral)
            timeout: Request timeout in seconds
        """
        self.logger = logging.getLogger("OllamaProvider")
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self.available = False
    
    def initialize(self) -> bool:
        """
        Initialize and verify Ollama connection.
        
        Returns:
            True if connected to Ollama, False otherwise
        """
        try:
            import requests
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                
                if self.model in model_names or any(self.model in m for m in model_names):
                    self.available = True
                    self.logger.info(f"Ollama initialized with model: {self.model}")
                    self.logger.info(f"Available models: {', '.join(model_names[:3])}...")
                    return True
                else:
                    self.logger.error(f"Model {self.model} not found in Ollama")
                    self.logger.info(f"Available models: {', '.join(model_names)}")
                    return False
            else:
                self.logger.error(f"Ollama returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama: {e}")
            self.logger.info("Make sure Ollama is running: ollama serve")
            return False
    
    async def chat(
        self,
        message: str,
        history: Optional[list[AIMessage]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Send message to Ollama and get response.
        
        Args:
            message: User message
            history: Conversation history
            system_prompt: System prompt for personality
        
        Returns:
            AI response
        """
        if not self.available:
            self.logger.error("Ollama provider not available")
            return "I'm not connected to Ollama. Please start Ollama first."
        
        try:
            # Build messages for context
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add conversation history
            if history:
                for msg in history:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call Ollama API
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "No response")
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                return "Sorry, I encountered an error processing your message."
                
        except Exception as e:
            self.logger.error(f"Chat error: {e}", exc_info=True)
            return f"I encountered an error: {str(e)}"
    
    def is_available(self) -> bool:
        """
        Check if Ollama provider is available.
        
        Returns:
            True if available, False otherwise
        """
        return self.available
