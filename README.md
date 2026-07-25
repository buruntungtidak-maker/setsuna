# Setsuna AI Desktop Companion 🎨

A modern AI-powered desktop pet application built with Python and PySide6. Features character rendering, emotion systems, browser integration, and voice capabilities.

## Features (Planned)

- 🎮 **Desktop Pet Character** - Animated character that lives on your desktop
- 🤖 **AI Integration** - OpenAI-compatible API support (OpenAI, Ollama, LM Studio, etc.)
- 💬 **Chat System** - Chat with your AI companion with memory and history
- 🎭 **Emotion System** - Character emotions change based on conversation
- 🌐 **Browser** - Integrated Qt WebEngine browser
- 🎨 **Layered Character** - Modular character parts (body, hair, outfit, etc.)
- 🎯 **Command System** - Intent detection for commands (YouTube, Google, etc.)
- 🔧 **Tool Calling** - Execute actions based on AI responses
- 🎵 **Voice Support** - Optional STT and TTS capabilities
- ⚙️ **Settings** - Configurable theme, language, AI provider, and more

## Project Structure

```
src/
├── core/                 # Core application logic
├── ai/                   # AI integration and models
├── browser/              # Browser functionality
├── character/            # Character rendering and management
├── animation/            # Animation system
├── emotion/              # Emotion system
├── assets/               # Static assets (images, etc.)
├── ui/                   # UI components and windows
├── voice/                # Speech synthesis and recognition
├── commands/             # Command registry and handlers
├── utils/                # Utility functions
├── services/             # Service layer
├── config/               # Configuration management
└── main.py               # Application entry point
```

## Requirements

- Python 3.11+
- PySide6
- OpenAI compatible API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/buruntungtidak-maker/setsuna.git
cd setsuna
```

2. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
cp config/config.example.json config/config.json
# Edit config/config.json and add your API key
```

5. Run the application:
```bash
python src/main.py
```

## Development Roadmap

- **Sprint 1** ✅ - Project Structure
- **Sprint 2** - Character Renderer
- **Sprint 3** - Animation System
- **Sprint 4** - Emotion System
- **Sprint 5** - Chat UI
- **Sprint 6** - AI Integration
- **Sprint 7** - Browser
- **Sprint 8** - Command System
- **Sprint 9** - Tool Calling
- **Sprint 10** - Memory
- **Sprint 11** - Voice
- **Sprint 12** - Optimization

## Architecture

This project follows **Clean Architecture** principles with:

- **Dependency Injection** - Loose coupling between modules
- **Service Layer** - Business logic separation
- **Factory Pattern** - Object creation
- **Observer Pattern** - Event handling
- **Command Pattern** - Command execution
- **Strategy Pattern** - Pluggable implementations

## Design Patterns Used

- Factory Pattern
- Observer Pattern
- Command Pattern
- Strategy Pattern
- Repository Pattern
- Service Locator

## Performance Targets

- CPU Usage: < 2%
- RAM Usage: < 300MB
- Animation FPS: 60
- Window: Transparent, Frameless, Always On Top

## Configuration

All settings are stored in `config/config.json`:

```json
{
  "ai": {
    "provider": "openai",
    "api_key": "your-key",
    "model": "gpt-4"
  },
  "character": {
    "name": "Setsuna",
    "scale": 1.0
  },
  "ui": {
    "theme": "dark",
    "language": "en"
  }
}
```

## License

MIT License

## Author

buruntungtidak-maker
