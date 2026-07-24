"""
Main: Application entry point for Setsuna AI Desktop Companion
"""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication
from src.core.application import Application, ApplicationConfig
from src.character import CharacterManager
from src.ui.main_window import MainWindow
from src.ai import AIService, OllamaProvider


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
        
        # Create core application
        app = Application(config)
        exit_code = app.run()
        
        if exit_code != 0:
            return exit_code
        
        # Initialize AI Service with Ollama
        ai_service = AIService(
            provider=OllamaProvider(
                base_url=app.config_manager.get("ai.base_url", "http://localhost:11434"),
                model=app.config_manager.get("ai.model", "mistral")
            )
        )
        
        if not ai_service.initialize():
            app.logger.warning("AI Service not available - running without chat functionality")
        else:
            app.logger.info("AI Service initialized successfully")
        
        # Initialize Character
        character_assets = Path("src/assets/characters/setsuna")
        
        # Create dummy assets if they don't exist
        if not character_assets.exists():
            app.logger.info("Creating default character assets structure...")
            _create_default_assets(character_assets)
        
        character_manager = CharacterManager(
            character_assets,
            name=app.config_manager.get("character.name", "Setsuna")
        )
        
        # Create Qt Application
        qt_app = QApplication(sys.argv)
        
        # Create main window
        window = MainWindow(
            character_manager,
            window_width=app.config_manager.get("ui.window_width", 400),
            window_height=app.config_manager.get("ui.window_height", 600)
        )
        window.show()
        
        app.logger.info("GUI started successfully")
        
        # Run Qt event loop
        return qt_app.exec()
        
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        return 1


def _create_default_assets(character_path: Path) -> None:
    """
    Create default character asset structure with placeholder images.
    
    Args:
        character_path: Path to character folder
    """
    from PIL import Image, ImageDraw
    
    # Create folders
    folders = ["body", "hair_front", "hair_back", "faces", "outfit", "accessories"]
    for folder in folders:
        (character_path / folder).mkdir(parents=True, exist_ok=True)
    
    # Create placeholder images
    size = (256, 256)
    colors = {
        "body": (255, 200, 150),      # Skin tone
        "hair_front": (180, 100, 0),  # Brown
        "hair_back": (180, 100, 0),   # Brown
        "faces": (0, 0, 0),            # Black
        "outfit": (100, 150, 255),    # Blue
        "accessories": (255, 215, 0), # Gold
    }
    
    for folder, color in colors.items():
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw circle based on folder
        if folder == "body":
            draw.ellipse([50, 20, 206, 180], fill=color, outline=(0, 0, 0, 255))
        elif folder == "faces":
            draw.ellipse([70, 50, 186, 150], fill=color, outline=(0, 0, 0, 255))
        else:
            draw.rectangle([60, 30, 196, 170], fill=color, outline=(0, 0, 0, 255))
        
        # Save image
        img_path = character_path / folder / f"{folder}_default.png"
        img.save(img_path)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
