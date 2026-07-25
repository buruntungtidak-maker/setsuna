"""
Character Part: Represents individual character parts (body, hair, etc.)
"""

from enum import Enum
from pathlib import Path
from typing import Optional
from PIL import Image
import logging


class PartType(Enum):
    """Character part types"""
    BODY = "body"
    HAIR_BACK = "hair_back"
    OUTFIT = "outfit"
    FACE = "face"
    HAIR_FRONT = "hair_front"
    ACCESSORY = "accessory"


class CharacterPart:
    """
    Represents a single character part (e.g., body_01, hair_front_02).
    
    Parts are composed together to create the full character sprite.
    """
    
    # Layer order for compositing (bottom to top)
    LAYER_ORDER = [
        PartType.BODY,
        PartType.OUTFIT,
        PartType.HAIR_BACK,
        PartType.FACE,
        PartType.HAIR_FRONT,
        PartType.ACCESSORY,
    ]
    
    def __init__(
        self,
        part_type: PartType,
        part_name: str,
        image_path: Path,
        size: tuple[int, int] = (256, 256)
    ):
        """
        Initialize character part.
        
        Args:
            part_type: Type of part (BODY, HAIR, etc.)
            part_name: Name identifier (e.g., "body_01")
            image_path: Path to PNG image
            size: Target size for part (width, height)
        """
        self.logger = logging.getLogger("CharacterPart")
        self.part_type = part_type
        self.part_name = part_name
        self.image_path = Path(image_path)
        self.size = size
        self.image: Optional[Image.Image] = None
        
        self._load_image()
    
    def _load_image(self) -> None:
        """
        Load PNG image from disk.
        """
        try:
            if not self.image_path.exists():
                self.logger.warning(f"Part image not found: {self.image_path}")
                return
            
            # Load and convert to RGBA (for transparency)
            self.image = Image.open(self.image_path).convert("RGBA")
            
            # Resize to target size
            self.image = self.image.resize(self.size, Image.Resampling.LANCZOS)
            
            self.logger.debug(f"Loaded part: {self.part_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load part image: {e}")
            self.image = None
    
    def get_image(self) -> Optional[Image.Image]:
        """
        Get the loaded image.
        
        Returns:
            PIL Image or None if not loaded
        """
        return self.image
    
    def is_loaded(self) -> bool:
        """
        Check if image is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return self.image is not None
    
    def get_layer_order(self) -> int:
        """
        Get layer order for this part type.
        
        Lower numbers are rendered first (bottom layer).
        
        Returns:
            Layer order index
        """
        return self.LAYER_ORDER.index(self.part_type)
    
    @staticmethod
    def get_layer_order_for_type(part_type: PartType) -> int:
        """
        Get layer order for a part type.
        
        Args:
            part_type: Type of part
        
        Returns:
            Layer order index
        """
        return CharacterPart.LAYER_ORDER.index(part_type)
