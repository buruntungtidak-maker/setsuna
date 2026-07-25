"""
Main Window: Main application window
"""

import logging
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QSpinBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import Qt as QtGui

from src.character import CharacterManager, Emotion
from .graphics_widget import CharacterGraphicsWidget


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Displays character and controls.
    """
    
    def __init__(
        self,
        character_manager: CharacterManager,
        window_width: int = 400,
        window_height: int = 600
    ):
        """
        Initialize main window.
        
        Args:
            character_manager: Character manager instance
            window_width: Window width
            window_height: Window height
        """
        super().__init__()
        self.logger = logging.getLogger("MainWindow")
        
        self.character_manager = character_manager
        self.window_width = window_width
        self.window_height = window_height
        
        # Setup window
        self.setWindowTitle("Setsuna - AI Desktop Companion")
        self.setGeometry(100, 100, window_width, window_height)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
            QLabel {
                color: #cdd6f4;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Character graphics (Ini bagian yang diperbaiki)
        self.graphics_widget = CharacterGraphicsWidget(
            "assets",  # <- Menggunakan string path untuk folder aset
            self       # <- Menambahkan self sebagai parent
        )
        main_layout.addWidget(self.graphics_widget)
        
        # Control panel
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)
        
        # Emotion buttons
        emotions = [
            ("Happy", Emotion.HAPPY),
            ("Sad", Emotion.SAD),
            ("Angry", Emotion.ANGRY),
            ("Laughing", Emotion.LAUGHING),
        ]
        
        for emotion_name, emotion in emotions:
            btn = QPushButton(emotion_name)
            btn.clicked.connect(lambda checked, e=emotion: self.set_emotion(e))
            control_layout.addWidget(btn)
        
        # Scale slider
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Scale:"))
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setMinimum(50)
        self.scale_slider.setMaximum(300)
        self.scale_slider.setValue(100)
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
        scale_layout.addWidget(self.scale_slider)
        control_layout.addLayout(scale_layout)
        
        self.logger.info("MainWindow initialized")
    
    def set_emotion(self, emotion: Emotion) -> None:
        """
        Set character emotion.
        
        Args:
            emotion: Emotion to set
        """
        self.character_manager.set_emotion(emotion)
        self.graphics_widget.update_character()
    
    def on_scale_changed(self, value: int) -> None:
        """
        Handle scale slider change.
        
        Args:
            value: New scale value (0-300)
        """
        scale = value / 100.0
        self.character_manager.set_scale(scale)