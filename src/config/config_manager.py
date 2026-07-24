"""
ConfigManager: Handles application configuration loading and saving
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class AIConfig:
    """AI configuration"""
    provider: str = "openai"
    api_key: str = ""
    model: str = "gpt-4"
    temperature: float = 0.7
    base_url: Optional[str] = None


@dataclass
class CharacterConfig:
    """Character configuration"""
    name: str = "Setsuna"
    scale: float = 1.0
    opacity: float = 1.0


@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "dark"
    language: str = "en"
    window_width: int = 400
    window_height: int = 500


@dataclass
class AudioConfig:
    """Audio configuration"""
    enabled: bool = True
    volume: int = 70
    tts_enabled: bool = True
    stt_enabled: bool = True


@dataclass
class Config:
    """Main configuration container"""
    ai: AIConfig
    character: CharacterConfig
    ui: UIConfig
    audio: AudioConfig


class ConfigManager:
    """
    Configuration manager for loading/saving JSON configuration.
    
    Supports automatic loading, saving, and default values.
    """
    
    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize ConfigManager.
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config_path = Path(config_path)
        self.logger = logging.getLogger("ConfigManager")
        self.config = self._create_default_config()
    
    @staticmethod
    def _create_default_config() -> Config:
        """Create default configuration."""
        return Config(
            ai=AIConfig(),
            character=CharacterConfig(),
            ui=UIConfig(),
            audio=AudioConfig()
        )
    
    def load(self) -> bool:
        """
        Load configuration from JSON file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not self.config_path.exists():
                self.logger.warning(f"Config file not found at {self.config_path}, using defaults")
                self._ensure_config_dir()
                self.save()
                return True
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load configuration data
            self.config = Config(
                ai=AIConfig(**data.get('ai', {})),
                character=CharacterConfig(**data.get('character', {})),
                ui=UIConfig(**data.get('ui', {})),
                audio=AudioConfig(**data.get('audio', {}))
            )
            
            self.logger.info("Configuration loaded successfully")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}", exc_info=True)
            return False
    
    def save(self) -> bool:
        """
        Save configuration to JSON file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            self._ensure_config_dir()
            
            config_dict = {
                'ai': asdict(self.config.ai),
                'character': asdict(self.config.character),
                'ui': asdict(self.config.ui),
                'audio': asdict(self.config.audio)
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            
            self.logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}", exc_info=True)
            return False
    
    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'ai.provider')
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    value = getattr(value, k, None)
                
                if value is None:
                    return default
            
            return value
        except (AttributeError, KeyError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'ai.provider')
            value: Value to set
        
        Returns:
            True if set successfully, False otherwise
        """
        try:
            keys = key.split('.')
            obj = self.config
            
            for k in keys[:-1]:
                obj = getattr(obj, k)
            
            setattr(obj, keys[-1], value)
            return True
        except (AttributeError, KeyError) as e:
            self.logger.error(f"Failed to set config key {key}: {e}")
            return False
