"""
CharacterScanner: Scans file system for character definitions and assets
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CharacterInfo:
    """Information about a discovered character"""
    name: str
    path: Path
    config_path: Optional[Path] = None
    config: Dict[str, Any] = field(default_factory=dict)
    asset_categories: Dict[str, Path] = field(default_factory=dict)
    

class CharacterScanner:
    """
    Scans the file system for character definitions and assets.
    
    Responsibilities:
    - Discover character folders
    - Load character configurations
    - Identify asset categories
    - Build character metadata
    """
    
    def __init__(self, assets_dir: Path):
        """
        Initialize CharacterScanner.
        
        Args:
            assets_dir: Root directory containing character assets
        """
        self.assets_dir = Path(assets_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.characters: Dict[str, CharacterInfo] = {}
    
    def scan(self) -> Dict[str, CharacterInfo]:
        """
        Scan assets directory for characters.
        
        Returns:
            Dictionary of character name -> CharacterInfo
        """
        self.characters.clear()
        
        if not self.assets_dir.exists():
            self.logger.warning(f"Assets directory does not exist: {self.assets_dir}")
            return self.characters
        
        characters_dir = self.assets_dir / "characters"
        if not characters_dir.exists():
            self.logger.warning(f"Characters directory does not exist: {characters_dir}")
            return self.characters
        
        # Scan each character folder
        for char_folder in characters_dir.iterdir():
            if not char_folder.is_dir():
                continue
            
            char_name = char_folder.name
            char_info = self._scan_character(char_name, char_folder)
            if char_info:
                self.characters[char_name] = char_info
                self.logger.debug(f"Discovered character: {char_name}")
        
        return self.characters
    
    def _scan_character(self, char_name: str, char_path: Path) -> Optional[CharacterInfo]:
        """
        Scan a single character folder.
        
        Args:
            char_name: Character name
            char_path: Path to character folder
        
        Returns:
            CharacterInfo or None if invalid
        """
        try:
            char_info = CharacterInfo(
                name=char_name,
                path=char_path
            )
            
            # Look for config.json
            config_path = char_path / "config.json"
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        char_info.config = json.load(f)
                    char_info.config_path = config_path
                except json.JSONDecodeError as e:
                    self.logger.error(f"Invalid JSON in {config_path}: {e}")
                    return None
            
            # Discover asset categories (subdirectories)
            for item in char_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    char_info.asset_categories[item.name] = item
            
            return char_info
            
        except Exception as e:
            self.logger.error(f"Error scanning character {char_name}: {e}")
            return None
    
    def get_character(self, name: str) -> Optional[CharacterInfo]:
        """
        Get character info by name.
        
        Args:
            name: Character name
        
        Returns:
            CharacterInfo or None if not found
        """
        return self.characters.get(name)
    
    def list_characters(self) -> List[str]:
        """
        Get list of all discovered characters.
        
        Returns:
            List of character names
        """
        return list(self.characters.keys())
