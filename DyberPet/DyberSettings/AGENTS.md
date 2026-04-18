# DyberSettings Module

**Path:** `DyberPet/DyberSettings/`  
**Purpose:** Settings panels and control windows

## STRUCTURE
```
DyberSettings/
├── DyberControlPanel.py   # Main settings window (3677 lines)
├── BasicSettingUI.py      # General settings tab
├── CharCardUI.py          # Character selection cards
├── PetCardUI.py           # Pet management cards
├── ItemCardUI.py          # Item card displays
├── GameSaveUI.py          # Save/load/backup UI
├── custom_base.py         # Base widget classes
├── custom_combobox.py     # Custom dropdowns
├── custom_utils.py        # UI utilities (6949 lines)
└── fileOp_utils.py        # File operations
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Open settings | `DyberControlPanel.py` | ControlMainWindow class |
| Basic settings | `BasicSettingUI.py` | Language, scale, theme color |
| Character cards | `CharCardUI.py` | Select/change pet character |
| Save management | `GameSaveUI.py` | Export/import/backup saves |
| Custom widgets | `custom_*.py` | Reusable UI components |

## CONVENTIONS
- Each tab is a separate class (BasicSettingInterface, etc.)
- Uses `qfluentwidgets` SettingCardGroup for organization
- Signal-based updates to main pet widget

## ANTI-PATTERNS
- `custom_utils.py` is very large (6949 lines) - split recommended
- Some UI logic mixed with data operations
</content>