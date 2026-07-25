"""
CharacterLoader: Loads and manages character state
"""

import logging
from pathlib import Path
from typing import Optional, Dict
import json

from .character_scanner import CharacterScanner
from .asset_database import AssetDatabase
from .asset_manager import AssetManager


class CharacterLoader:
    """
    Loads and manages character data, assets, and state.
    
    Responsibilities:
    - Load character configuration
    - Discover and cache assets
    - Manage asset selections
    - Provide character metadata
    - Handle character switching
    """
    
    def __init__(self, assets_dir: Path):
        """
        Initialize CharacterLoader.
        
        Args:
            assets_dir: Root assets directory
        """
        self.assets_dir = Path(assets_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.scanner = CharacterScanner(assets_dir)
        self.asset_database: Optional[AssetDatabase] = None
        self.asset_manager: Optional[AssetManager] = None
        
        self.current_character: Optional[str] = None
        self.character_config: Dict = {}
        self.layer_order: list = []
    
    def discover_characters(self) -> list:
        """
        Discover all available characters.
        
        Returns:
            List of character names
        """
        characters = self.scanner.scan()
        return self.scanner.list_characters()
    
    def load_character(self, character_name: str) -> bool:
        """
        Load a character by name.
        
        Args:
            character_name: Name of character to load
        
        Returns:
            True if successful
        """
        try:
            char_info = self.scanner.get_character(character_name)
            if not char_info:
                self.logger.error(f"Character not found: {character_name}")
                return False
            
            self.current_character = character_name
            
            # Load character configuration
            self.character_config = char_info.config or {}
            
            # Extract layer order from config
            self.layer_order = self.character_config.get('layer_order', [])
            if not self.layer_order:
                # Auto-detect from asset categories
                self.layer_order = sorted(char_info.asset_categories.keys())
            
            self.logger.info(f"Loaded character config for {character_name}")
            
            # Initialize asset database
            self.asset_database = AssetDatabase(char_info.path)
            self.asset_database.scan()
            
            self.logger.info(f"Scanned {len(self.asset_database.list_categories())} asset categories")
            
            # Initialize asset manager
            self.asset_manager = AssetManager(char_info.path, self.asset_database)
            self.asset_manager.load_selections()
            
            self.logger.info(f"Loaded asset selections for {character_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load character {character_name}: {e}")
            return False
    
    def get_character_path(self) -> Optional[Path]:
        """Get path to currently loaded character."""
        if self.current_character:
            char_info = self.scanner.get_character(self.current_character)
            if char_info:
                return char_info.path
        return None
    
    def get_layer_order(self) -> list:
        """Get layer rendering order for current character."""
        return self.layer_order.copy()
    
    def get_selected_asset_path(self, category: str) -> Optional[Path]:
        """
        Get path to currently selected asset for category.
        
        Args:
            category: Asset category
        
        Returns:
            Path to asset file/folder or None
        """
        if self.asset_manager:
            return self.asset_manager.get_asset_path(category)
        return None
    
    def set_asset(self, category: str, asset_name: str) -> bool:
        """
        Set asset selection for category.
        
        Args:
            category: Asset category
            asset_name: Asset name to select
        
        Returns:
            True if successful
        """
        if self.asset_manager:
            return self.asset_manager.set_asset(category, asset_name)
        return False
    
    def get_available_assets(self, category: str) -> list:
        """
        Get list of available assets for category.
        
        Args:
            category: Asset category
        
        Returns:
            List of asset names
        """
        if self.asset_database:
            return self.asset_database.list_assets(category)
        return []
    
    def get_asset_categories(self) -> list:
        """Get all asset categories for current character."""
        if self.asset_database:
            return self.asset_database.list_categories()
        return []
    
    def get_character_scale(self) -> float:
        """Get character scale from configuration."""
        return self.character_config.get('scale', 1.0)
    
    def get_character_opacity(self) -> float:
        """Get character opacity from configuration."""
        return self.character_config.get('opacity', 1.0)
