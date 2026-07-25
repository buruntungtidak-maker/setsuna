"""
Character Manager: Manages character state, animations, and rendering
"""

from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass, field
import logging
from enum import Enum

from .character_sprite import CharacterSprite
from .character_part import PartType


class Emotion(Enum):
    """Character emotion states"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    CONFUSED = "confused"
    LAUGHING = "laughing"


@dataclass
class CharacterState:
    """Character state snapshot"""
    name: str = "Setsuna"
    emotion: Emotion = Emotion.NEUTRAL
    position: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    scale: float = 1.0
    opacity: float = 1.0
    is_sleeping: bool = False
    is_moving: bool = False


class CharacterManager:
    """
    Character manager for state and sprite management.
    
    Handles:
    - Character sprite composition and rendering
    - Emotion system and expression changes
    - Character state and animations
    - Asset management
    """
    
    def __init__(
        self,
        character_path: Path,
        name: str = "Setsuna",
        size: Tuple[int, int] = (256, 256)
    ):
        """
        Initialize character manager.
        
        Args:
            character_path: Path to character assets folder
            name: Character name
            size: Sprite size (width, height)
        """
        self.logger = logging.getLogger("CharacterManager")
        self.character_path = Path(character_path)
        self.size = size
        
        # Initialize state
        self.state = CharacterState(name=name)
        
        # Initialize sprite
        self.sprite = CharacterSprite(character_path, size)
        
        # Emotion to face part mapping
        self.emotion_faces = {
            Emotion.NEUTRAL: "face_neutral.png",
            Emotion.HAPPY: "face_happy.png",
            Emotion.SAD: "face_sad.png",
            Emotion.ANGRY: "face_angry.png",
            Emotion.SURPRISED: "face_surprised.png",
            Emotion.CONFUSED: "face_confused.png",
            Emotion.LAUGHING: "face_laughing.png",
        }
        
        self.logger.info(f"CharacterManager initialized: {name}")
    
    def set_emotion(self, emotion: Emotion) -> bool:
        """
        Change character emotion and corresponding face.
        
        Args:
            emotion: New emotion
        
        Returns:
            True if emotion changed successfully, False otherwise
        """
        try:
            self.state.emotion = emotion
            
            # Try to load corresponding face
            face_name = self.emotion_faces.get(emotion, "face_neutral.png")
            face_path = self.character_path / "faces" / face_name
            
            if face_path.exists():
                self.sprite.change_part(PartType.FACE, face_path)
                self.logger.info(f"Emotion changed to: {emotion.value}")
                return True
            else:
                self.logger.warning(f"Face not found for emotion {emotion.value}")
                # Try first available face
                available_faces = self.sprite.get_available_parts(PartType.FACE)
                if available_faces:
                    self.sprite.change_part(PartType.FACE, available_faces[0])
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to set emotion: {e}")
            return False
    
    def set_position(self, x: int, y: int) -> None:
        """
        Set character position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.state.position = (x, y)
    
    def set_scale(self, scale: float) -> None:
        """
        Set character scale.
        
        Args:
            scale: Scale factor (1.0 = 100%)
        """
        self.state.scale = max(0.1, min(3.0, scale))  # Clamp between 0.1 and 3.0
    
    def set_opacity(self, opacity: float) -> None:
        """
        Set character opacity.
        
        Args:
            opacity: Opacity (0.0 = invisible, 1.0 = fully visible)
        """
        self.state.opacity = max(0.0, min(1.0, opacity))  # Clamp between 0 and 1
    
    def set_sleeping(self, sleeping: bool) -> None:
        """
        Set character sleep state.
        
        Args:
            sleeping: True if sleeping, False otherwise
        """
        self.state.is_sleeping = sleeping
        if sleeping:
            self.set_emotion(Emotion.NEUTRAL)  # Change to neutral face when sleeping
            self.logger.info("Character is sleeping")
        else:
            self.logger.info("Character woke up")
    
    def set_moving(self, moving: bool) -> None:
        """
        Set character movement state.
        
        Args:
            moving: True if moving, False otherwise
        """
        self.state.is_moving = moving
    
    def get_composed_image(self):
        """
        Get current composed character sprite.
        
        Returns:
            PIL Image of composed character
        """
        return self.sprite.get_composed_image()
    
    def get_state(self) -> CharacterState:
        """
        Get current character state.
        
        Returns:
            Character state object
        """
        return self.state
    
    def change_outfit(self, outfit_name: str) -> bool:
        """
        Change character outfit.
        
        Args:
            outfit_name: Name of outfit file (without path)
        
        Returns:
            True if successful, False otherwise
        """
        outfit_path = self.character_path / "outfit" / outfit_name
        return self.sprite.change_part(PartType.OUTFIT, outfit_path)
    
    def change_accessory(self, accessory_name: str) -> bool:
        """
        Change character accessory.
        
        Args:
            accessory_name: Name of accessory file (without path)
        
        Returns:
            True if successful, False otherwise
        """
        accessory_path = self.character_path / "accessories" / accessory_name
        return self.sprite.change_part(PartType.ACCESSORY, accessory_path)
