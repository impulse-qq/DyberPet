# DyberPet Project Knowledge Base

**Generated:** 2025-04-19  
**Commit:** a769d14  
**Branch:** main  

## OVERVIEW
DyberPet (呆啵宠物) is a PySide6-based desktop pet application framework. Version 0.7.7.

## STRUCTURE
```
DyberPet/
├── run_DyberPet.py           # Entry point - launches QApplication
├── DyberPet/                 # Main package (doubly-nested)
│   ├── DyberPet.py           # Core PetWidget (2085 lines)
│   ├── Dashboard/            # Dashboard UI subpackage
│   ├── DyberSettings/        # Settings panel subpackage
│   ├── conf.py               # Data classes (PetData, ActData, ItemData)
│   ├── modules.py            # Animation and interaction modules
│   └── ...
├── res/                      # Resources (images, sounds, JSON configs)
│   ├── role/                 # Pet character definitions
│   ├── items/                # Item definitions
│   └── language/             # i18n translation files
└── docs/                     # Documentation
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Entry point | `run_DyberPet.py` | QApplication setup, signal wiring |
| Main pet widget | `DyberPet/DyberPet.py` | PetWidget class, drag/animation logic |
| Pet config | `res/role/<name>/pet_conf.json` | Character stats, animations |
| Items | `res/items/<mod>/items_config.json` | Consumables, collections, buffs |
| Data classes | `DyberPet/conf.py` | PetConfig, PetData, TaskData, ActData |
| Settings | `DyberPet/settings.py` | Runtime config, paths, version |
| Dashboard UI | `DyberPet/Dashboard/` | Status, backpack, shop, tasks, animation |
| Settings UI | `DyberPet/DyberSettings/` | Control panel, character cards |

## CODE MAP
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| PetWidget | class | DyberPet/DyberPet.py | Main pet window, animations, interactions |
| DyberPetApp | class | run_DyberPet.py | QApplication subclass, system wiring |
| PetData | class | DyberPet/conf.py | Pet state persistence (HP, FV, items) |
| ActData | class | DyberPet/conf.py | Animation playlist management |
| ItemData | class | DyberPet/conf.py | Item definitions and buffs |
| DashboardMainWindow | class | Dashboard/DashboardUI.py | Main dashboard window |
| ControlMainWindow | class | DyberSettings/DyberControlPanel.py | Settings panel |

## CONVENTIONS
- **Imports:** Absolute imports from `DyberPet.*` package
- **Qt Style:** Uses PySide6-Fluent-Widgets for UI components
- **Config:** JSON files for content, Python constants for runtime
- **Naming:** Snake_case for functions, PascalCase for classes
- **Architecture:** Signal/slot pattern for component communication

## ANTI-PATTERNS (THIS PROJECT)
- **No tests:** Zero test infrastructure (no pytest, unittest, test files)
- **No CI/CD:** Manual builds only, no GitHub Actions
- **No requirements.txt:** Dependencies only in README install commands
- **Nested package:** Code in `DyberPet/DyberPet/` instead of flat structure
- **Magic numbers:** Hardcoded coordinates, timeouts in animation logic
- **Large files:** Several files >500 lines (DyberPet.py: 2085, extra_windows.py: 1152)

## UNIQUE STYLES
- **Pet system:** Characters defined via JSON configs in `res/role/`
- **Animation system:** Frame-based PNG sequences with anchor points
- **Buff system:** Temporary stat modifiers via items
- **FV/HP system:** Favorability (好感度) and Hunger (饱食度) mechanics
- **Bubble system:** Dialogue bubbles above pet with configurable triggers
- **Mini-pets:** Companion pets that follow main character

## COMMANDS
```bash
# Run from source
python run_DyberPet.py

# Build (Windows)
pyinstaller --noconsole --icon="000.ico" \
  --hidden-import="pynput.mouse._win32" \
  --hidden-import="pynput.keyboard._win32" \
  run_DyberPet.py

# Translation update
pylupdate5 langs.pro
lrelease langs.zh_CN.ts
```

## DEPENDENCIES
- Python 3.9+
- PySide6==6.5.2
- PySide6-Fluent-Widgets==1.5.4
- pynput (input monitoring)
- apscheduler (scheduled tasks)
- tendo (singleton instance)

## NOTES
- Single-instance enforced via tendo (prevents multiple processes)
- Data stored in `~/.config/DyberPet/DyberPet/data/`
- Supports Windows and macOS (no Linux packaging)
- LLM module mentioned in README but not open-sourced yet
- Process singleton enforced - cannot run multiple instances
- Midnight timer triggers daily events at 00:00
</content>