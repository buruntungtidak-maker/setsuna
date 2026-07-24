"""
Main: Application entry point for Setsuna AI Desktop Companion
"""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.application import Application, ApplicationConfig


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        Application exit code
    """
    try:
        # Configure application
        config = ApplicationConfig(
            config_path="config/config.json",
            log_level="INFO",
            debug=False
        )
        
        # Create and run application
        app = Application(config)
        exit_code = app.run()
        
        if exit_code == 0:
            app.logger.info("Setsuna started successfully")
            # Main GUI loop will be added in Sprint 5
            app.logger.info("GUI initialization pending (Sprint 5)")
        
        return exit_code
        
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
