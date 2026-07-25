"""
ExpressionController: Maps AI emotions to character expressions
"""

import logging
from typing import Dict, Optional
from enum import Enum


class Emotion(Enum):
    """AI emotion states"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    THINKING = "thinking"
    EXCITED = "excited"
    EMBARRASSED = "embarrassed"
    SLEEPY = "sleepy"
    CONFUSED = "confused"
    LISTENING = "listening"
    TALKING = "talking"


class ExpressionController:
    """
    Maps AI emotion states to character expressions.
    
    Responsibilities:
    - Receive emotion state from AI
    - Map emotion to expression assets
    - Synchronize eyes, eyebrows, mouth
    - Manage talking and blinking
    - Handle idle behavior
    """
    
    def __init__(self, asset_manager):
        """
        Initialize ExpressionController.
        
        Args:
            asset_manager: AssetManager instance
        """
        self.asset_manager = asset_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_emotion: Emotion = Emotion.NEUTRAL
        
        # Define emotion to asset mappings
        self.emotion_mapping: Dict[Emotion, Dict[str, str]] = {
            Emotion.NEUTRAL: {
                'eyes': 'normal',
                'eyebrows': 'normal',
                'mouth': 'normal',
            },
            Emotion.HAPPY: {
                'eyes': 'happy',
                'eyebrows': 'happy',
                'mouth': 'smile',
            },
            Emotion.SAD: {
                'eyes': 'sad',
                'eyebrows': 'sad',
                'mouth': 'sad',
            },
            Emotion.ANGRY: {
                'eyes': 'angry',
                'eyebrows': 'angry',
                'mouth': 'angry',
            },
            Emotion.SURPRISED: {
                'eyes': 'surprised',
                'eyebrows': 'surprised',
                'mouth': 'surprised',
            },
            Emotion.THINKING: {
                'eyes': 'thinking',
                'eyebrows': 'thinking',
                'mouth': 'thinking',
            },
            Emotion.EXCITED: {
                'eyes': 'excited',
                'eyebrows': 'excited',
                'mouth': 'smile',
            },
            Emotion.EMBARRASSED: {
                'eyes': 'embarrassed',
                'eyebrows': 'embarrassed',
                'mouth': 'embarrassed',
            },
            Emotion.SLEEPY: {
                'eyes': 'sleepy',
                'eyebrows': 'sleepy',
                'mouth': 'sleepy',
            },
            Emotion.CONFUSED: {
                'eyes': 'confused',
                'eyebrows': 'confused',
                'mouth': 'confused',
            },
            Emotion.LISTENING: {
                'eyes': 'listening',
                'eyebrows': 'normal',
                'mouth': 'normal',
            },
            Emotion.TALKING: {
                'eyes': 'normal',
                'eyebrows': 'normal',
                'mouth': 'talking',
            },
        }
    
    def set_emotion(self, emotion: Emotion) -> bool:
        """
        Set current emotion.
        
        Args:
            emotion: Emotion state
        
        Returns:
            True if successful
        """
        if emotion not in self.emotion_mapping:
            self.logger.warning(f"Unknown emotion: {emotion}")
            return False
        
        self.current_emotion = emotion
        return self._apply_emotion()
    
    def set_emotion_by_name(self, name: str) -> bool:
        """
        Set emotion by name string.
        
        Args:
            name: Emotion name (e.g., "happy", "sad")
        
        Returns:
            True if successful
        """
        try:
            emotion = Emotion[name.upper()]
            return self.set_emotion(emotion)
        except KeyError:
            self.logger.warning(f"Unknown emotion name: {name}")
            return False
    
    def _apply_emotion(self) -> bool:
        """
        Apply current emotion by setting assets.
        
        Returns:
            True if successful
        """
        try:
            mapping = self.emotion_mapping.get(self.current_emotion, {})
            
            for category, asset_name in mapping.items():
                if self.asset_manager:
                    if not self.asset_manager.set_asset(category, asset_name):
                        self.logger.warning(
                            f"Could not set asset {category}/{asset_name}"
                        )
            
            self.logger.debug(f"Applied emotion: {self.current_emotion.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying emotion: {e}")
            return False
    
    def get_current_emotion(self) -> Emotion:
        """Get current emotion."""
        return self.current_emotion
    
    def get_current_emotion_name(self) -> str:
        """Get current emotion name."""
        return self.current_emotion.value
