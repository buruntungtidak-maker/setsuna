"""
Character Sprite: Composes multiple parts into complete character sprite
"""

from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import logging

from .character_part import CharacterPart, PartType


class CharacterSprite:
    """
    Character sprite composed of multiple layered parts.
    
    Automatically loads and composes PNG parts from character folder.
    Supports dynamic changing of parts (e.g., different outfits, emotions).
    """
    
    def __init__(
        self,
        character_path: Path,
        size: tuple[int, int] = (256, 256)
    ):
        """
        Initialize character sprite.
        
        Args:
            character_path: Path to character folder (e.g., src/assets/characters/setsuna/)
            size: Target sprite size (width, height)
        """
        self.logger = logging.getLogger("CharacterSprite")
        self.character_path = Path(character_path)
        self.size = size
        self.parts: Dict[PartType, CharacterPart] = {}
        self.composed_image: Optional[Image.Image] = None
        
        self._load_parts()
    
    def _load_parts(self) -> None:
        """
        Load all available parts from character folder.
        
        Scans folders: body/, hair_front/, hair_back/, faces/, outfit/, accessories/
        """
        try:
            # Map folder names to part types
            folder_map = {
                "body": PartType.BODY,
                "hair_front": PartType.HAIR_FRONT,
                "hair_back": PartType.HAIR_BACK,
                "faces": PartType.FACE,
                "outfit": PartType.OUTFIT,
                "accessories": PartType.ACCESSORY,
            }
            
            # Load first available part from each folder
            for folder_name, part_type in folder_map.items():
                folder_path = self.character_path / folder_name
                
                if not folder_path.exists():
                    self.logger.warning(f"Folder not found: {folder_path}")
                    continue
                
                # Find first PNG file
                png_files = list(folder_path.glob("*.png"))
                
                if png_files:
                    # Use first PNG file
                    image_path = png_files[0]
                    part_name = image_path.stem
                    
                    part = CharacterPart(
                        part_type=part_type,
                        part_name=part_name,
                        image_path=image_path,
                        size=self.size
                    )
                    
                    if part.is_loaded():
                        self.parts[part_type] = part
                        self.logger.debug(f"Loaded {folder_name}: {part_name}")
                else:
                    self.logger.warning(f"No PNG files in: {folder_path}")
            
            self.logger.info(f"Loaded {len(self.parts)} character parts")
            
        except Exception as e:
            self.logger.error(f"Failed to load parts: {e}", exc_info=True)
    
    def compose(self) -> Optional[Image.Image]:
        """
        Compose all parts into single character sprite.
        
        Layers are composed in correct order (bottom to top).
        
        Returns:
            Composed PIL Image or None if composition failed
        """
        try:
            # Create transparent base
            composed = Image.new("RGBA", self.size, (0, 0, 0, 0))
            
            # Sort parts by layer order
            sorted_parts = sorted(
                self.parts.values(),
                key=lambda p: p.get_layer_order()
            )
            
            # Composite each part
            for part in sorted_parts:
                if part.is_loaded():
                    image = part.get_image()
                    if image:
                        composed.paste(image, (0, 0), image)
            
            self.composed_image = composed
            self.logger.debug("Character sprite composed")
            return composed
            
        except Exception as e:
            self.logger.error(f"Composition failed: {e}", exc_info=True)
            return None
    
    def get_composed_image(self) -> Optional[Image.Image]:
        """
        Get latest composed image.
        
        Returns:
            Composed PIL Image or None
        """
        if self.composed_image is None:
            return self.compose()
        return self.composed_image
    
    def change_part(
        self,
        part_type: PartType,
        image_path: Path
    ) -> bool:
        """
        Change a specific character part.
        
        Args:
            part_type: Type of part to change
            image_path: Path to new image
        
        Returns:
            True if successful, False otherwise
        """
        try:
            part = CharacterPart(
                part_type=part_type,
                part_name=image_path.stem,
                image_path=image_path,
                size=self.size
            )
            
            if part.is_loaded():
                self.parts[part_type] = part
                self.composed_image = None  # Invalidate cache
                self.logger.info(f"Changed {part_type.value}: {image_path.name}")
                return True
            else:
                self.logger.error(f"Failed to load new part: {image_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to change part: {e}")
            return False
    
    def get_available_parts(self, part_type: PartType) -> List[Path]:
        """
        Get available parts of a specific type.
        
        Args:
            part_type: Type of part
        
        Returns:
            List of available PNG paths
        """
        try:
            folder_map = {
                PartType.BODY: "body",
                PartType.HAIR_FRONT: "hair_front",
                PartType.HAIR_BACK: "hair_back",
                PartType.FACE: "faces",
                PartType.OUTFIT: "outfit",
                PartType.ACCESSORY: "accessories",
            }
            
            folder_name = folder_map.get(part_type)
            if not folder_name:
                return []
            
            folder_path = self.character_path / folder_name
            if not folder_path.exists():
                return []
            
            return sorted(list(folder_path.glob("*.png")))
            
        except Exception as e:
            self.logger.error(f"Failed to get available parts: {e}")
            return []
