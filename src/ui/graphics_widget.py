"""
Graphics Widget: QGraphicsView for rendering character
"""

import logging
from pathlib import Path
from PIL import Image
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer, QSize
from typing import Optional

from src.character import CharacterManager


class CharacterGraphicsWidget(QGraphicsView):
    """
    QGraphicsView widget for displaying character sprite.
    
    Handles rendering, scaling, and animation updates.
    """
    
    def __init__(
        self,
        character_manager: CharacterManager,
        width: int = 400,
        height: int = 500
    ):
        """
        Initialize graphics widget.
        
        Args:
            character_manager: Character manager instance
            width: Widget width
            height: Widget height
        """
        super().__init__()
        self.logger = logging.getLogger("CharacterGraphicsWidget")
        
        self.character_manager = character_manager
        self.width = width
        self.height = height
        
        # Setup scene
        self.scene = QGraphicsScene(0, 0, width, height)
        self.setScene(self.scene)
        
        # Character pixmap item
        self.character_item: Optional[QGraphicsPixmapItem] = None
        
        # Setup widget
        self.setRenderHint(QGraphicsView.RenderHint.SmoothPixmapTransform)
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
    
    def pil_to_pixmap(self, pil_image: Image.Image) -> QPixmap:
        """
        Convert PIL Image to QPixmap.
        
        Args:
            pil_image: PIL Image object
        
        Returns:
            QPixmap for Qt rendering
        """
        # Convert RGBA to RGBA for proper transparency
        if pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")
        
        # Convert to QImage
        data = pil_image.tobytes("raw", "RGBA")
        q_image = QImage(
            data,
            pil_image.width,
            pil_image.height,
            QImage.Format.Format_RGBA8888
        )
        
        return QPixmap.fromImage(q_image)
    
    def update_character(self) -> None:
        """
        Update character rendering.
        
        Called periodically for animation updates.
        """
        try:
            # Get composed image
            pil_image = self.character_manager.get_composed_image()
            
            if pil_image is None:
                self.logger.warning("Failed to get composed image")
                return
            
            # Convert to QPixmap
            pixmap = self.pil_to_pixmap(pil_image)
            
            # Apply scale
            state = self.character_manager.get_state()
            scaled_size = QSize(
                int(self.character_manager.size[0] * state.scale),
                int(self.character_manager.size[1] * state.scale)
            )
            pixmap = pixmap.scaledToWidth(scaled_size.width())
            
            # Remove old item
            if self.character_item:
                self.scene.removeItem(self.character_item)
            
            # Add new item
            self.character_item = self.scene.addPixmap(pixmap)
            
            # Center in scene
            self.character_item.setPos(
                (self.width - pixmap.width()) / 2,
                (self.height - pixmap.height()) / 2
            )
            
        except Exception as e:
            self.logger.error(f"Failed to update character: {e}", exc_info=True)
    
    def set_character_scale(self, scale: float) -> None:
        """
        Set character scale.
        
        Args:
            scale: Scale factor
        """
        self.character_manager.set_scale(scale)
