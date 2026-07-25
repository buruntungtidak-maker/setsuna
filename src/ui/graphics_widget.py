"""
CharacterGraphicsWidget: PySide6 graphics widget for rendering character
"""

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from src.character.character_loader import CharacterLoader
from src.character.layer_renderer import LayerRenderer


class CharacterGraphicsWidget(QGraphicsView):
    """
    Graphics widget for displaying rendered character.
    
    Responsibilities:
    - Display character on screen
    - Handle scaling and positioning
    - Manage graphics scene
    - Support layer composition
    """
    
    def __init__(self, assets_dir: Path, character_name: str = "Setsuna"):
        """
        Initialize CharacterGraphicsWidget.
        
        Args:
            assets_dir: Path to assets directory
            character_name: Name of character to load
        """
        super().__init__()
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.assets_dir = Path(assets_dir)
        self.character_name = character_name
        
        # Initialize components
        self.character_loader = CharacterLoader(assets_dir)
        self.layer_renderer = LayerRenderer(Path(assets_dir) / "characters" / character_name)
        self.current_pixmap_item: Optional[QGraphicsPixmapItem] = None
        
        # Setup graphics scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Configure view properties
        # Note: QGraphicsView handles rendering hints automatically
        # No need to set RenderHint on QGraphicsView itself
        self.setStyleSheet("QGraphicsView { border: none; background: transparent; }")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        


        # Setup widget
        self.setrenderHint(QGraphicsView.renderHint.SmoothPixmapTransform)
        self.setStyleSheet("background: transparent;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setMinimumSize(width, height)
        
        # Refresh timer for animation
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_character)
        self.refresh_timer.start(16)  # ~60 FPS
        
        # Initial render
        self.update_character()
        self.logger.debug("CharacterGraphicsWidget initialized")
        
        self.logger.debug("CharacterGraphicsWidget initialized")
    

    def load_character(self) -> bool:
        """
        Load character and render to scene.
        
        Returns:
            True if successful
        """
        try:
            # Load character data
            if not self.character_loader.load_character(self.character_name):
                self.logger.error(f"Failed to load character: {self.character_name}")
                return False
            
            self.logger.info(f"Character loaded: {self.character_name}")
            
            # Render character
            return self.render_character()
            
        except Exception as e:
            self.logger.error(f"Error loading character: {e}", exc_info=True)
            return False
    
    def render_character(self) -> bool:
        """
        Render character layers and display.
        
        Returns:
            True if successful
        """
        try:
            layer_order = self.character_loader.get_layer_order()
            scale = self.character_loader.get_character_scale()
            
            # Build layer paths dictionary
            layer_paths = {}
            for category in layer_order:
                asset_path = self.character_loader.get_selected_asset_path(category)
                if asset_path:
                    layer_paths[category] = asset_path
            
            if not layer_paths:
                self.logger.error("No layers to render")
                return False
            
            # Render layers
            pil_image = self.layer_renderer.render(
                layer_paths=layer_paths,
                layer_order=layer_order,
                scale=scale,
                background_color=(0, 0, 0, 0)
            )
            
            if not pil_image:
                self.logger.error("Failed to render layers")
                return False
            
            # Convert PIL image to QPixmap
            qimage = self._pil_to_qimage(pil_image)
            pixmap = QPixmap.fromImage(qimage)
            
            # Update scene
            self.display_pixmap(pixmap)
            
            self.logger.info(f"Character rendered: {pixmap.width()}x{pixmap.height()}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error rendering character: {e}", exc_info=True)
            return False
    
    def display_pixmap(self, pixmap: QPixmap) -> None:
        """
        Display pixmap in scene.
        
        Args:
            pixmap: QPixmap to display
        """
        try:
            # Clear previous item
            if self.current_pixmap_item:
                self.scene.removeItem(self.current_pixmap_item)
            
            # Add new item
            self.current_pixmap_item = self.scene.addPixmap(pixmap)
            self.current_pixmap_item.setPos(0, 0)
            
            # Adjust scene rect to pixmap
            self.scene.setSceneRect(self.current_pixmap_item.boundingRect())
            
            self.logger.debug("Pixmap displayed in scene")
            
        except Exception as e:
            self.logger.error(f"Error displaying pixmap: {e}", exc_info=True)
    
    @staticmethod
    def _pil_to_qimage(pil_image) -> QImage:
        """
        Convert PIL Image to QImage.
        
        Args:
            pil_image: PIL Image object
        
        Returns:
            QImage
        """
        # Convert to RGBA if not already
        if pil_image.mode != 'RGBA':
            pil_image = pil_image.convert('RGBA')
        
        # Get image data
        width, height = pil_image.size
        data = pil_image.tobytes('raw', 'RGBA')
        
        # Create QImage
        qimage = QImage(data, width, height, QImage.Format.Format_RGBA8888)
        
        return qimage
