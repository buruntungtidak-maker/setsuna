"""
LayerRenderer: Composes character from independent layers
"""

import logging
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import Image


class LayerRenderer:
    """
    Renders character by composing independent layers.
    
    Responsibilities:
    - Load individual layer images
    - Compose layers in correct order
    - Apply scaling
    - Handle transparency
    - Cache composed images
    - Support animation frames
    """
    
    def __init__(self, character_path: Path):
        """
        Initialize LayerRenderer.
        
        Args:
            character_path: Path to character folder
        """
        self.character_path = Path(character_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.image_cache: dict = {}
    
    def render(
        self,
        layer_paths: List[Path],
        layer_order: List[str],
        scale: float = 1.0,
        background_color: Tuple[int, int, int, int] = (0, 0, 0, 0)
    ) -> Optional[Image.Image]:
        """
        Render character by composing layers.
        
        Args:
            layer_paths: Dictionary mapping layer names to their paths
            layer_order: Order in which to composite layers
            scale: Scale factor for final image
            background_color: RGBA background color
        
        Returns:
            Composed PIL Image or None if failed
        """
        try:
            # Load all layer images
            layers = {}
            max_width = 0
            max_height = 0
            
            for layer_name in layer_order:
                if layer_name not in layer_paths:
                    self.logger.warning(f"Layer path not provided for: {layer_name}")
                    continue
                
                layer_path = layer_paths[layer_name]
                img = self._load_layer_image(layer_name, layer_path)
                
                if img:
                    layers[layer_name] = img
                    max_width = max(max_width, img.width)
                    max_height = max(max_height, img.height)
            
            if not layers:
                self.logger.error("No layers loaded successfully")
                return None
            
            # Create base canvas
            base = Image.new('RGBA', (max_width, max_height), background_color)
            
            # Composite layers in order
            for layer_name in layer_order:
                if layer_name in layers:
                    base = Image.alpha_composite(base, layers[layer_name])
            
            # Apply scaling if needed
            if scale != 1.0:
                new_width = int(base.width * scale)
                new_height = int(base.height * scale)
                base = base.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.logger.debug(f"Rendered character: {base.width}x{base.height}")
            return base
            
        except Exception as e:
            self.logger.error(f"Error rendering character: {e}")
            return None
    
    def _load_layer_image(self, layer_name: str, layer_path: Path) -> Optional[Image.Image]:
        """
        Load a single layer image.
        
        Args:
            layer_name: Name of layer
            layer_path: Path to layer file or folder
        
        Returns:
            PIL Image or None
        """
        try:
            # Check cache first
            cache_key = str(layer_path)
            if cache_key in self.image_cache:
                return self.image_cache[cache_key].copy()
            
            # If it's a file, load it directly
            if layer_path.is_file():
                img = Image.open(layer_path).convert('RGBA')
                self.image_cache[cache_key] = img.copy()
                return img
            
            # If it's a directory, try to load first frame
            if layer_path.is_dir():
                pngs = sorted(layer_path.glob('*.png'))
                if pngs:
                    img = Image.open(pngs[0]).convert('RGBA')
                    self.image_cache[cache_key] = img.copy()
                    return img
            
            self.logger.warning(f"Could not load layer image: {layer_path}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading layer {layer_name} from {layer_path}: {e}")
            return None
    
    def clear_cache(self) -> None:
        """Clear image cache."""
        self.image_cache.clear()
