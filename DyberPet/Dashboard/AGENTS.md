# Dashboard Module

**Path:** `DyberPet/Dashboard/`  
**Purpose:** Main dashboard UI - status, inventory, shop, tasks, animation editor

## STRUCTURE
```
Dashboard/
├── DashboardUI.py         # Main dashboard window (5164 lines)
├── dashboard_widgets.py   # Shared widgets (1271 lines)
├── statusUI.py            # HP/FV status panel
├── inventoryUI.py         # Backpack/inventory grid
├── shopUI.py              # Item shop interface
├── taskUI.py              # Focus timer, Pomodoro, todos
├── animationUI.py         # Animation player panel
├── animDesignUI.py        # Animation editor (4490 lines)
└── buffModule.py          # Buff calculation logic
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Open dashboard | `DashboardUI.py` | DashboardMainWindow class |
| Status panel | `statusUI.py` | HP/FV bars, level badges |
| Backpack grid | `inventoryUI.py` | Draggable item slots |
| Shop interface | `shopUI.py` | Buy/sell with coin system |
| Focus timer | `taskUI.py` | Pomodoro, focus mode |
| Animation player | `animationUI.py` | Play custom animations |
| Animation editor | `animDesignUI.py` | Create/edit animations |
| Buff effects | `buffModule.py` | HP_stop, FV_boost, etc. |

## CONVENTIONS
- Extends `qfluentwidgets` components (CardWidget, ScrollArea, etc.)
- Uses `Signal` for cross-panel communication
- Grid layouts for inventory (draggable slots)
- List widgets for shop items with filtering

## ANTI-PATTERNS
- `animDesignUI.py` is very large (4490 lines) - consider splitting
- Hardcoded UI strings in Chinese (mixed with English)
- TODO at line 309: "prevent negative amount of coins"
</content>