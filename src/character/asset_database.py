"""
AssetDatabase: Manages discovery and caching of all character assets
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class AssetInfo:
    """Information about a single asset"""
    name: str
    path: Path
    category: str
    is_default: bool = False
    is_animated: bool = False
    is_frame_sequence: bool = False
    frames: List[Path] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class AssetCategory:
    """Information about an asset category"""
    name: str
    path: Path
    assets: Dict[str, AssetInfo] = field(default_factory=dict)
    default_asset: Optional[AssetInfo] = None


class AssetDatabase:
    """
    Manages discovery, caching, and retrieval of character assets.
    
    Responsibilities:
    - Automatically discover all assets in character folders
    - Detect default assets (_default naming convention)
    - Identify animated asset sequences
    - Cache asset metadata
    - Load asset.json metadata when available
    - Handle asset renaming without code changes
    """
    
    def __init__(self, character_path: Path):
        """
        Initialize AssetDatabase.
        
        Args:
            character_path: Path to character folder
        """
        self.character_path = Path(character_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.categories: Dict[str, AssetCategory] = {}
        self._cached: bool = False
    
    def scan(self) -> Dict[str, AssetCategory]:
        """
        Scan character folder for all assets.
        
        Returns:
            Dictionary of category name -> AssetCategory
        """
        self.categories.clear()
        
        if not self.character_path.exists():
            self.logger.error(f"Character path does not exist: {self.character_path}")
            return self.categories
        
        # Scan each subdirectory as a category
        for category_path in self.character_path.iterdir():
            if not category_path.is_dir() or category_path.name.startswith('.'):
                continue
            
            category_name = category_path.name
            category = self._scan_category(category_name, category_path)
            if category and category.assets:
                self.categories[category_name] = category
                self.logger.debug(f"Discovered category: {category_name} with {len(category.assets)} assets")
        
        self._cached = True
        return self.categories
    
    def _scan_category(self, category_name: str, category_path: Path) -> Optional[AssetCategory]:
        """
        Scan a single category folder.
        
        Args:
            category_name: Category name (folder name)
            category_path: Path to category folder
        
        Returns:
            AssetCategory or None if no valid assets found
        """
        try:
            category = AssetCategory(
                name=category_name,
                path=category_path
            )
            
            # Collect all items in category
            png_files: Dict[str, Path] = {}
            animation_folders: Dict[str, Path] = {}
            
            for item in category_path.iterdir():
                if item.name.startswith('.'):
                    continue
                
                if item.is_file() and item.suffix.lower() == '.png':
                    png_files[item.stem] = item
                elif item.is_dir():
                    animation_folders[item.name] = item
            
            # Process static PNG files
            for stem, png_path in png_files.items():
                is_default = stem.endswith('_default')
                asset_name = stem.replace('_default', '') if is_default else stem
                
                # Load metadata if available
                metadata = self._load_metadata(png_path)
                
                asset = AssetInfo(
                    name=asset_name,
                    path=png_path,
                    category=category_name,
                    is_default=is_default or metadata.get('default', False),
                    metadata=metadata
                )
                
                category.assets[asset_name] = asset
            
            # Process animation folders
            for anim_name, anim_path in animation_folders.items():
                frames = self._detect_frame_sequence(anim_path)
                
                if frames:
                    is_default = anim_name.endswith('_default')
                    asset_name = anim_name.replace('_default', '') if is_default else anim_name
                    
                    # Load metadata if available
                    metadata = self._load_metadata(anim_path)
                    
                    asset = AssetInfo(
                        name=asset_name,
                        path=anim_path,
                        category=category_name,
                        is_default=is_default or metadata.get('default', False),
                        is_animated=True,
                        is_frame_sequence=True,
                        frames=frames,
                        metadata=metadata
                    )
                    
                    category.assets[asset_name] = asset
                    self.logger.debug(f"Detected animation: {asset_name} with {len(frames)} frames")
            
            # Set default asset
            category.default_asset = self._find_default_asset(category)
            if category.default_asset:
                self.logger.debug(f"Category '{category_name}' default: {category.default_asset.name}")
            
            return category
            
        except Exception as e:
            self.logger.error(f"Error scanning category {category_name}: {e}")
            return None
    
    def _detect_frame_sequence(self, anim_path: Path) -> List[Path]:
        """
        Detect frame sequence in animation folder.
        
        Looks for PNG files following patterns:
        - name_01.png, name_02.png, name_03.png
        - name_001.png, name_002.png, name_003.png
        
        Args:
            anim_path: Path to animation folder
        
        Returns:
            Sorted list of frame paths
        """
        frames: List[Path] = []
        
        try:
            for png_file in sorted(anim_path.glob('*.png')):
                if not png_file.name.startswith('.'):
                    frames.append(png_file)
            
            return frames
        except Exception as e:
            self.logger.error(f"Error detecting frames in {anim_path}: {e}")
            return []
    
    def _load_metadata(self, asset_path: Path) -> Dict:
        """
        Load asset.json metadata if available.
        
        Args:
            asset_path: Path to asset file or folder
        
        Returns:
            Dictionary of metadata or empty dict
        """
        try:
            # For files, check sibling directory
            if asset_path.is_file():
                metadata_path = asset_path.parent / f"{asset_path.stem}.json"
            else:
                # For directories
                metadata_path = asset_path / "asset.json"
            
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.debug(f"Could not load metadata from {metadata_path}: {e}")
        
        return {}
    
    def _find_default_asset(self, category: AssetCategory) -> Optional[AssetInfo]:
        """
        Find default asset for category.
        
        Priority:
        1. Asset with is_default=True
        2. First discovered asset (alphabetically)
        
        Args:
            category: AssetCategory to search
        
        Returns:
            AssetInfo of default asset or None
        """
        # First, look for explicitly marked defaults
        for asset in category.assets.values():
            if asset.is_default:
                return asset
        
        # Fall back to first asset
        if category.assets:
            first_name = sorted(category.assets.keys())[0]
            return category.assets[first_name]
        
        return None
    
    def get_category(self, category_name: str) -> Optional[AssetCategory]:
        """
        Get asset category by name.
        
        Args:
            category_name: Category name
        
        Returns:
            AssetCategory or None
        """
        return self.categories.get(category_name)
    
    def get_asset(self, category: str, asset_name: str) -> Optional[AssetInfo]:
        """
        Get specific asset by category and name.
        
        Args:
            category: Category name
            asset_name: Asset name
        
        Returns:
            AssetInfo or None
        """
        cat = self.categories.get(category)
        if cat:
            return cat.assets.get(asset_name)
        return None
    
    def get_default_asset(self, category: str) -> Optional[AssetInfo]:
        """
        Get default asset for category.
        
        Args:
            category: Category name
        
        Returns:
            AssetInfo of default or None
        """
        cat = self.categories.get(category)
        if cat:
            return cat.default_asset
        return None
    
    def list_categories(self) -> List[str]:
        """Get list of all categories."""
        return sorted(self.categories.keys())
    
    def list_assets(self, category: str) -> List[str]:
        """Get list of all assets in category."""
        cat = self.categories.get(category)
        if cat:
            return sorted(cat.assets.keys())
        return []
