# Sprint 1: Project Structure Guide

## Overview

Sprint 1 establishes the complete project foundation with clean architecture, modular structure, and professional setup following SOLID principles.

## What Was Created

### 1. **Project Structure**

```
setsuna/
├── src/
│   ├── core/                    # Core application lifecycle
│   │   ├── __init__.py
│   │   └── application.py       # Main Application class
│   │
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   └── config_manager.py    # JSON config handler
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   └── logger.py            # Logging setup
│   │
│   ├── ai/                      # AI module (Sprint 6)
│   ├── browser/                 # Browser module (Sprint 7)
│   ├── character/               # Character module (Sprint 2)
│   ├── animation/               # Animation module (Sprint 3)
│   ├── emotion/                 # Emotion module (Sprint 4)
│   ├── ui/                      # UI module (Sprint 5)
│   ├── voice/                   # Voice module (Sprint 11)
│   ├── commands/                # Commands module (Sprint 8)
│   ├── services/                # Services module
│   │
│   ├── assets/                  # Static assets
│   │   └── characters/
│   │       └── setsuna/
│   │           ├── body/
│   │           ├── hair_front/
│   │           ├── hair_back/
│   │           ├── faces/
│   │           ├── outfit/
│   │           └── accessories/
│   │
│   └── main.py                  # Application entry point
│
├── config/
│   ├── config.example.json      # Configuration template
│   └── config.json              # Actual config (created on first run)
│
├── logs/                        # Log files (auto-created)
├── tests/                       # Test files (future)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables template
├── README.md                    # Project documentation
└── SPRINT_1_GUIDE.md           # This file
```

### 2. **Core Components**

#### **Application Class** (`src/core/application.py`)
- Manages application lifecycle
- Initializes services
- Handles configuration loading
- Provides logging interface

**Design Pattern**: Service Locator / Application Service

```python
app = Application(ApplicationConfig(config_path="config/config.json"))
exit_code = app.run()
```

#### **ConfigManager** (`src/config/config_manager.py`)
- Loads/saves JSON configuration
- Type-safe with dataclasses
- Supports dot-notation access
- Auto-creates default configs

**Design Pattern**: Repository Pattern

```python
config_manager = ConfigManager("config/config.json")
config_manager.load()
api_key = config_manager.get("ai.api_key")
```

#### **Logger Setup** (`src/utils/logger.py`)
- Centralized logging configuration
- Console and file output
- Rotating file handlers
- Structured formatting

**Features**:
- Auto-creates logs directory
- 10MB rotating files with 5 backups
- Consistent timestamp formatting

### 3. **Configuration System**

**Config Structure** (JSON):
```json
{
  "ai": {
    "provider": "openai",
    "api_key": "sk-...",
    "model": "gpt-4",
    "temperature": 0.7,
    "base_url": null
  },
  "character": {
    "name": "Setsuna",
    "scale": 1.0,
    "opacity": 1.0
  },
  "ui": {
    "theme": "dark",
    "language": "en",
    "window_width": 400,
    "window_height": 500
  },
  "audio": {
    "enabled": true,
    "volume": 70,
    "tts_enabled": true,
    "stt_enabled": true
  }
}
```

**Dataclasses Used**:
- `AIConfig` - AI provider settings
- `CharacterConfig` - Character appearance
- `UIConfig` - UI theme and window
- `AudioConfig` - Audio settings
- `Config` - Main container

### 4. **Design Principles Applied**

✅ **Single Responsibility Principle (SRP)**
- Each class has one responsibility
- `Application` → lifecycle
- `ConfigManager` → configuration
- `Logger` → logging

✅ **Open/Closed Principle (OCP)**
- Modular structure allows extension
- New modules can be added without modifying existing ones

✅ **Liskov Substitution Principle (LSP)**
- Dataclass-based configuration allows flexible substitution

✅ **Interface Segregation Principle (ISP)**
- Small, focused interfaces
- ConfigManager has clear get/set methods

✅ **Dependency Inversion Principle (DIP)**
- Application accepts ApplicationConfig
- Services are injected, not hard-coded

### 5. **File Organization**

**Module Structure**:
- Each major feature gets its own module (e.g., `ai/`, `browser/`)
- Each module has `__init__.py` for clean imports
- `.placeholder` files mark future sprint work

**Benefits**:
- Clear separation of concerns
- Easy to find code
- Scalable for team development
- Prevents circular imports

### 6. **Documentation**

- **README.md** - Project overview and setup instructions
- **requirements.txt** - All dependencies pinned to versions
- **.gitignore** - Excludes generated files and secrets
- **config.example.json** - Configuration template
- **.env.example** - Environment variable template
- **Docstrings** - All functions have detailed docstrings

## How to Use

### 1. **Setup Development Environment**

```bash
# Clone repository
git clone https://github.com/buruntungtidak-maker/setsuna.git
cd setsuna

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration template
cp config/config.example.json config/config.json

# Add your OpenAI API key to config/config.json
```

### 2. **Run Application**

```bash
python src/main.py
```

**Expected Output**:
```
2024-01-15 10:30:45 - Setsuna - INFO - Setsuna AI Desktop Companion initializing...
2024-01-15 10:30:45 - Setsuna - DEBUG - Loading configuration...
2024-01-15 10:30:45 - Setsuna - INFO - Configuration loaded successfully
2024-01-15 10:30:45 - Setsuna - INFO - Application initialized successfully
2024-01-15 10:30:45 - Setsuna - INFO - Application ready
```

### 3. **Access Configuration**

```python
from src.config.config_manager import ConfigManager

config = ConfigManager("config/config.json")
config.load()

# Get values
api_key = config.get("ai.api_key")
theme = config.get("ui.theme")

# Set values
config.set("ui.theme", "light")
config.save()
```

### 4. **Logging**

```python
from src.utils.logger import setup_logger

logger = setup_logger("MyModule", level="DEBUG")
logger.info("Application started")
logger.debug("Debug information")
logger.error("An error occurred", exc_info=True)
```

## Architecture Decisions

### 1. **Why Dataclasses for Config?**
- Type-safe configuration
- Easy validation
- Clear structure
- Simple serialization/deserialization

### 2. **Why Modular Structure?**
- Clear separation of concerns
- Easy to test individual modules
- Team can work on different modules simultaneously
- Easy to replace modules (e.g., different AI providers)

### 3. **Why Repository Pattern for ConfigManager?**
- Abstracts storage mechanism
- Can easily switch from JSON to YAML, TOML, etc.
- Centralized configuration access

### 4. **Why Application Class?**
- Lifecycle management in one place
- Service initialization orchestration
- Clean entry point

## Testing the Setup

### 1. **Check Imports**
```python
python -c "from src.core.application import Application; print('✓ Core imports work')"
python -c "from src.config.config_manager import ConfigManager; print('✓ Config imports work')"
python -c "from src.utils.logger import setup_logger; print('✓ Utils imports work')"
```

### 2. **Verify Logging**
```bash
python -c "from src.utils.logger import setup_logger; logger = setup_logger('Test'); logger.info('Logging works!')"
# Check logs/Test.log was created
```

### 3. **Verify Configuration**
```bash
python -c "from src.config.config_manager import ConfigManager; cm = ConfigManager('config/config.json'); cm.load(); print(cm.config)"
```

## What's Ready for Sprint 2

- ✅ Project structure
- ✅ Configuration system
- ✅ Logging system
- ✅ Application lifecycle
- ✅ Type hints and docstrings
- ✅ Clean architecture foundation

**Not Ready Yet** (Planned for future sprints):
- ❌ Character rendering (Sprint 2)
- ❌ Animation system (Sprint 3)
- ❌ Emotion system (Sprint 4)
- ❌ Chat UI (Sprint 5)
- ❌ AI integration (Sprint 6)

## Common Issues & Fixes

### Issue: `ModuleNotFoundError: No module named 'src'`
**Fix**: Make sure you're running from the project root directory

### Issue: `config/config.json not found`
**Fix**: Run `python src/main.py` once - it auto-creates the file from defaults

### Issue: Logs not being created
**Fix**: Make sure `logs/` directory is writable (or let application create it)

## Next Steps (Sprint 2)

Sprint 2 will focus on:
1. Character rendering system with layered parts
2. QGraphicsView/QGraphicsScene setup
3. Asset loading and caching
4. Character composition from PNG parts
5. Basic movement and positioning

The foundation is now ready for building the rendering system!

---

**Sprint Status**: ✅ COMPLETE
**Lines of Code**: ~600
**Modules Created**: 8
**Documentation**: Complete
**Ready for Sprint 2**: YES
