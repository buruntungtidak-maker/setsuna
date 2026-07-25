"""
AssetManager: Manages asset selection, loading, and persistence
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class AssetSelection:
    """Current asset selection state"""
    character: str
    selections: Dict[str, str]  # category -> asset_name


class AssetManager:
    """
    Manages asset selection and persistence.
    
    Responsibilities:
    - Store user-selected assets per character
    - Save selections to selection.json
    - Load selections on startup
    - Provide current selection state
    - Handle invalid selections gracefully
    """
    
    def __init__(self, character_path: Path, asset_database):
        """
        Initialize AssetManager.
        
        Args:
            character_path: Path to character folder
            asset_database: AssetDatabase instance
        """
        self.character_path = Path(character_path)
        self.asset_database = asset_database
        self.logger = logging.getLogger(self.__class__.__name__)
        self.selection_file = character_path / "selection.json"
        self.current_selection: Dict[str, str] = {}
    
    def load_selections(self) -> Dict[str, str]:
        """
        Load asset selections from selection.json.
        
        If file doesn't exist, use all defaults.
        
        Returns:
            Dictionary of category -> asset_name
        """
        self.current_selection.clear()
        
        # Initialize with defaults
        for category_name in self.asset_database.list_categories():
            default_asset = self.asset_database.get_default_asset(category_name)
            if default_asset:
                self.current_selection[category_name] = default_asset.name
        
        # Try to load selections file
        if self.selection_file.exists():
            try:
                with open(self.selection_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                
                # Merge saved selections, validating each one
                for category, asset_name in saved.items():
                    asset = self.asset_database.get_asset(category, asset_name)
                    if asset:
                        self.current_selection[category] = asset_name
                    else:
                        self.logger.warning(
                            f"Invalid asset selection: {category}/{asset_name}, using default"
                        )
                
                self.logger.info("Asset selections loaded successfully")
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in selections file: {e}")
            except Exception as e:
                self.logger.error(f"Error loading selections: {e}")
        
        return self.current_selection
    
    def save_selections(self) -> bool:
        """
        Save current selections to selection.json.
        
        Returns:
            True if successful
        """
        try:
            self.character_path.mkdir(parents=True, exist_ok=True)
            
            with open(self.selection_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_selection, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Asset selections saved successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error saving selections: {e}")
            return False
    
    def set_asset(self, category: str, asset_name: str) -> bool:
        """
        Set selected asset for category.
        
        Args:
            category: Category name
            asset_name: Asset name to select
        
        Returns:
            True if valid selection
        """
        asset = self.asset_database.get_asset(category, asset_name)
        if asset:
            self.current_selection[category] = asset_name
            self.save_selections()
            return True
        else:
            self.logger.warning(f"Invalid asset: {category}/{asset_name}")
            return False
    
    def get_asset(self, category: str) -> Optional[str]:
        """
        Get currently selected asset name for category.
        
        Args:
            category: Category name
        
        Returns:
            Asset name or None
        """
        return self.current_selection.get(category)
    
    def get_asset_path(self, category: str) -> Optional[Path]:
        """
        Get path to currently selected asset.
        
        Args:
            category: Category name
        
        Returns:
            Path to asset or None
        """
        asset_name = self.current_selection.get(category)
        if asset_name:
            asset = self.asset_database.get_asset(category, asset_name)
            if asset:
                return asset.path
        return None
    
    def get_all_selections(self) -> Dict[str, str]:
        """Get all current selections."""
        return self.current_selection.copy()
