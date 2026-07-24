"""
Application: Main application class for Setsuna
Handles initialization, lifecycle, and service management
"""

import logging
from typing import Optional
from dataclasses import dataclass

from src.config.config_manager import ConfigManager
from src.utils.logger import setup_logger


@dataclass
class ApplicationConfig:
    """Application configuration container"""
    config_path: str = "config/config.json"
    log_level: str = "INFO"
    debug: bool = False


class Application:
    """
    Main application class.
    
    Manages application lifecycle, service initialization, and configuration.
    
    Attributes:
        config_manager: Configuration management service
        logger: Application logger
    """
    
    def __init__(self, app_config: Optional[ApplicationConfig] = None):
        """
        Initialize the application.
        
        Args:
            app_config: Application configuration. Defaults to ApplicationConfig()
        """
        self.app_config = app_config or ApplicationConfig()
        self.logger = setup_logger("Setsuna", self.app_config.log_level)
        self.config_manager: Optional[ConfigManager] = None
        
        self.logger.info("Setsuna AI Desktop Companion initializing...")
    
    def initialize(self) -> bool:
        """
        Initialize all application services.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.debug("Loading configuration...")
            self.config_manager = ConfigManager(self.app_config.config_path)
            self.config_manager.load()
            
            self.logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}", exc_info=True)
            return False
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Application exit code
        """
        if not self.initialize():
            return 1
        
        self.logger.info("Application ready")
        return 0
    
    def shutdown(self) -> None:
        """Shutdown the application gracefully."""
        self.logger.info("Shutting down Setsuna...")
        # Cleanup will be added in future sprints
