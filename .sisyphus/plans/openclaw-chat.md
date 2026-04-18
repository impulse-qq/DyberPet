# OpenClaw Chat Integration for DyberPet

## TL;DR

> **Quick Summary**: Add a side-panel chat dialog to DyberPet that connects to a local OpenAI-compatible LLM gateway (OpenClaw at http://localhost:18789/v1). Users click a right-click menu item to open a chat panel next to their pet, configure the model name and system prompt in settings, and have in-memory-only conversations with non-streaming responses.
>
> **Deliverables**:
> - `DyberPet/ChatPanel/` sub-package with chat UI and API worker
> - Right-click menu integration in `PetWidget`
> - Settings integration (api_url, model_name, system_prompt)
> - Signal wiring in `run_DyberPet.py`
>
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Task 1 (settings) → Task 3 (ChatPanel) → Task 5 (wiring) → Task 6 (menu)

---

## Context

### Original Request
Add a chat dialog feature to DyberPet desktop pet. Users click to show a side panel where they can chat with OpenClaw (local LLM gateway with OpenAI-compatible endpoint). No streaming, no persistence, configurable model name and system prompt.

### Interview Summary
**Key Discussions**:
- API endpoint: `http://localhost:18789/v1` (OpenAI-compatible)
- UI style: Side panel (not floating bubble, not full window)
- Response mode: Wait for full response (no streaming)
- System prompt: User-configurable (not auto-injected from pet_conf.json)
- Chat history: In-memory only, no persistence across sessions
- Model name: Configurable in settings

**Research Findings**:
- Existing UI pattern: `DashboardMainWindow` and `ControlMainWindow` as independent QWidget windows
- Signal wiring: All done in `DyberPetApp.__connectSignalToSlot()` in `run_DyberPet.py`
- Right-click menu: Built in `PetWidget._set_Statusmenu()` using `RoundMenu`
- Settings: Module-level globals in `settings.py`, JSON read/write for persistence
- No existing requirements.txt — dependencies only documented in README
- The project has NO test infrastructure

### Metis Review
**Identified Gaps (addressed)**:
- URL trailing slash bug: Added normalization in settings
- QThread vs QRunnable: Using httpx in QRunnable worker for lighter dependency
- Screen edge clamping: Added boundary check logic
- Input disabled during response: Added explicit guard
- No requirements.txt: Create one with httpx dependency
- Error UX: Show error messages in chat area, not toast
- Chat history cap: 100 messages max, trim oldest
- i18n: Use `self.tr()` for all user-visible strings

---

## Work Objectives

### Core Objective
Integrate OpenClaw LLM chat functionality into DyberPet as a side panel, matching existing project architecture and UI patterns.

### Concrete Deliverables
- `DyberPet/ChatPanel/__init__.py` — Package init
- `DyberPet/ChatPanel/ChatUI.py` — ChatMainWindow, ChatPanel widget, message display
- `DyberPet/ChatPanel/ChatWorker.py` — QRunnable-based API call worker with httpx
- `DyberPet/ChatPanel/ChatSettings.py` — Settings UI tab for API/config
- Modified `DyberPet/DyberPet.py` — Add `show_chat` Signal, menu action in `_set_Statusmenu`
- Modified `DyberPet/settings.py` — Add `api_url`, `model_name`, `system_prompt` globals
- Modified `run_DyberPet.py` — Import, instantiate, wire ChatMainWindow
- `requirements.txt` — Add httpx dependency

### Definition of Done
- [ ] Right-click on pet shows "Chat" menu item
- [ ] Clicking "Chat" opens side panel adjacent to pet
- [ ] Chat panel has input field, send button, message display area
- [ ] Sending a message calls the OpenAI-compatible endpoint and displays response
- [ ] Settings page allows configuring api_url, model_name, system_prompt
- [ ] Settings persist across app restarts
- [ ] UI does not freeze during API calls
- [ ] Error messages appear in chat area when endpoint is unreachable
- [ ] Chat history is cleared on panel close (in-memory only)
- [ ] Chat input is disabled while waiting for LLM response

### Must Have
- Side panel chat UI adjacent to pet
- OpenAI-compatible API call via httpx (non-streaming)
- QRunnable + QThreadPool for non-blocking API calls
- Right-click menu integration
- Settings persistence for api_url, model_name, system_prompt
- Error handling for unreachable endpoint
- Chat input disabled during response wait
- Chat history capped at 100 messages (trim oldest)
- URL trailing slash normalization

### Must NOT Have (Guardrails)
- NO streaming support (explicitly excluded)
- NO chat history persistence to disk
- NO system prompt injection from pet_conf.json
- NO markdown rendering in chat responses
- NO model parameters (temperature, top_p, etc.) in settings
- NO token counting or cost tracking
- NO openai SDK dependency (use httpx only)
- NO QThread subclass pattern (use QRunnable)
- NO API calls on the main thread
- NO fullscreen or bubble-style UI

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO
- **Automated tests**: NONE (no test framework)
- **Agent-Executed QA**: ALWAYS (mandatory for all tasks)

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Desktop App UI**: Use Bash (python import checks + grep verification)
- **API Worker**: Use Bash (python import + class hierarchy checks)
- **Settings**: Use Bash (grep + JSON validation)
- **Integration**: Use Bash (python import chain + signal wiring grep)

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - foundation + settings):
├── Task 1: Chat settings in settings.py [quick]
├── Task 2: ChatWorker with httpx [deep]
└── Task 3: ChatPanel UI widgets [visual-engineering]

Wave 2 (After Wave 1 - integration):
├── Task 4: ChatSettings UI tab [visual-engineering]
├── Task 5: Signal wiring in run_DyberPet.py [quick]
└── Task 6: Right-click menu integration [quick]

Wave FINAL (After ALL tasks — 4 parallel reviews):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
```

### Dependency Matrix

| Task | Depends On | Blocks |
|------|------------|--------|
| 1 | - | 4, 5 |
| 2 | - | 5 |
| 3 | - | 4, 5 |
| 4 | 1, 3 | 5 |
| 5 | 1, 2, 3, 4 | 6 |
| 6 | 5 | - |

### Agent Dispatch Summary

- **Wave 1**: 3 tasks — T1 `quick`, T2 `deep`, T3 `visual-engineering`
- **Wave 2**: 3 tasks — T4 `visual-engineering`, T5 `quick`, T6 `quick`
- **FINAL**: 4 tasks — F1 `oracle`, F2 `unspecified-high`, F3 `unspecified-high`, F4 `deep`

---

## TODOs

- [x] 1. Add chat settings globals to settings.py

  **What to do**:
  - Add three new module-level globals to `DyberPet/settings.py`: `api_url = "http://localhost:18789/v1/"`, `model_name = ""`, `system_prompt = ""`
  - Add these to `init_settings()` using `data_params.get('api_url', 'http://localhost:18789/v1/')` pattern (follow existing pattern for `gravity`, `volume`, etc.)
  - Add these to `save_settings()` in the `data_js` dict
  - Add URL normalization: ensure `api_url` always ends with `/` — if user provides without trailing slash, append it
  - Add `chat_on = True` toggle (consistent with `bubble_on` pattern)
  - Find the exact lines where `init_settings()` reads settings and `save_settings()` writes them by reading `settings.py`

  **Must NOT do**:
  - Do NOT add temperature, top_p, max_tokens or other model parameters
  - Do NOT create a separate settings file — extend the existing one
  - Do NOT use the openai SDK — httpx only

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - **Skills Evaluated but Omitted**: `visual-engineering` (no UI in this task)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 4, 5
  - **Blocked By**: None (can start immediately)

  **References**:

  **Pattern References** (existing code to follow):
  - `DyberPet/settings.py:init_settings()` — Read pattern with `data_params.get('key', default)` for each setting
  - `DyberPet/settings.py:save_settings()` — Write pattern rebuilding `data_js` dict
  - `DyberPet/settings.py:gravity`, `DyberPet/settings.py:volume` — Module-level global pattern

  **API/Type References**:
  - `DyberPet/settings.py:CONFIGDIR` — Where settings.json is stored (`~/.config/DyberPet/DyberPet/data/`)

  **WHY Each Reference Matters**:
  - `init_settings()` and `save_settings()` define the EXACT pattern for adding settings — must follow identically
  - Existing globals show where to add new ones (near related settings, alphabetical or grouped)
  - `CONFIGDIR` shows where the JSON file is persisted

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Settings globals are defined and importable
    Tool: Bash
    Preconditions: DyberPet settings module is importable
    Steps:
      1. Run: python -c "import DyberPet.settings as s; s.init(); assert hasattr(s, 'api_url'); assert hasattr(s, 'model_name'); assert hasattr(s, 'system_prompt'); assert hasattr(s, 'chat_on'); print('OK')"
      2. Assert output contains "OK"
    Expected Result: All four new globals are accessible
    Failure Indicators: ImportError, AttributeError
    Evidence: .sisyphus/evidence/task-1-settings-import.txt

  Scenario: API URL normalization strips/appends trailing slash
    Tool: Bash
    Preconditions: settings.py is modified
    Steps:
      1. Run: python -c "import DyberPet.settings as s; s.init(); assert s.api_url.endswith('/'), f'URL does not end with /: {s.api_url}'; print('OK')"
    Expected Result: api_url always ends with /
    Failure Indicators: AssertionError
    Evidence: .sisyphus/evidence/task-1-url-normalization.txt

  Scenario: Settings persist to JSON and reload correctly
    Tool: Bash
    Preconditions: App has been run at least once
    Steps:
      1. Grep settings.json for the new keys: grep -c "api_url\|model_name\|system_prompt\|chat_on" ~/.config/DyberPet/DyberPet/data/settings.json
      2. Assert count is >= 4
    Expected Result: All 4 settings appear in JSON file
    Failure Indicators: Count < 4
    Evidence: .sisyphus/evidence/task-1-settings-persist.txt
  ```

  **Commit**: YES (group with this task only)
  - Message: `feat(settings): add chat settings globals (api_url, model_name, system_prompt)`
  - Files: `DyberPet/settings.py`
  - Pre-commit: `python -c "import DyberPet.settings as s; s.init(); print('OK')"`

- [x] 2. Create ChatWorker for LLM API calls (httpx + QRunnable)

  **What to do**:
  - Create `DyberPet/ChatPanel/` directory with `__init__.py`
  - Create `DyberPet/ChatPanel/ChatWorker.py` with a `ChatWorker(QRunnable)` class
  - The worker should:
    - Accept `messages` (list of dicts), `api_url` (str), `model_name` (str) as constructor params
    - Use `httpx` to POST to `{api_url}chat/completions` with `{"model": model_name, "messages": messages, "stream": False}`
    - Emit `response_received = Signal(str)` on success with the assistant's message content
    - Emit `error_occurred = Signal(str)` on failure with error description
    - Handle connection errors, timeout errors, and non-200 responses gracefully
    - Set a reasonable timeout (30 seconds)
    - Create httpx.Client inside `run()`, NOT as a shared instance (thread safety)
  - Create `requirements.txt` at project root with `httpx>=0.24.0` and all existing dependencies from README
  - ChatWorker must NOT use the openai SDK — raw httpx POST only

  **Must NOT do**:
  - Do NOT use the openai SDK package
  - Do NOT implement streaming (stream=False only)
  - Do NOT share httpx.Client instances across threads
  - Do NOT call API on the main thread

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []
  - **Skills Evaluated but Omitted**: `visual-engineering` (no UI in this task)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 5
  - **Blocked By**: None (can start immediately)

  **References**:

  **Pattern References** (existing code to follow):
  - `DyberPet/Dashboard/buffModule.py:BuffThread(QThread)` — Threading pattern for background work (note: we use QRunnable instead, but the signal emit pattern is the same)
  - `DyberPet/DyberPet.py:Animation_worker(QObject)` — Worker-with-signals pattern moved to QThread

  **API/Type References**:
  - OpenAI Chat Completions API: `POST /v1/chat/completions` with `{"model": str, "messages": [{"role": "user", "content": str}], "stream": false}`
  - Response format: `{"choices": [{"message": {"role": "assistant", "content": str}, "finish_reason": str}]}`
  - Error format: `{"error": {"message": str, "type": str}}`

  **External References**:
  - httpx documentation: https://www.python-httpx.org/ — HTTP client for Python with timeout and connection pooling

  **WHY Each Reference Matters**:
  - `BuffThread` shows the project's existing thread pattern with PySide6 signals
  - OpenAI API reference defines the exact request/response shape the worker must construct/parse
  - httpx is the chosen HTTP client (lighter than openai SDK)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ChatWorker imports and is a QRunnable subclass
    Tool: Bash
    Preconditions: DyberPet/ChatPanel/ChatWorker.py exists
    Steps:
      1. Run: python -c "from PySide6.QtCore import QRunnable; from DyberPet.ChatPanel.ChatWorker import ChatWorker; assert issubclass(ChatWorker, QRunnable); print('OK')"
      2. Assert output contains "OK"
    Expected Result: ChatWorker is importable and subclasses QRunnable
    Failure Indicators: ImportError, AssertionError
    Evidence: .sisyphus/evidence/task-2-worker-import.txt

  Scenario: ChatWorker has required signals
    Tool: Bash
    Preconditions: ChatWorker is importable
    Steps:
      1. Run: python -c "from DyberPet.ChatPanel.ChatWorker import ChatWorker; assert hasattr(ChatWorker, 'response_received'); assert hasattr(ChatWorker, 'error_occurred'); print('OK')"
    Expected Result: Both signals are defined on the class
    Failure Indicators: AttributeError
    Evidence: .sisyphus/evidence/task-2-worker-signals.txt

  Scenario: HTTP call uses non-streaming mode
    Tool: Bash (grep)
    Preconditions: ChatWorker.py is written
    Steps:
      1. Run: grep -n "stream" DyberPet/ChatPanel/ChatWorker.py
      2. Verify "stream" appears with value False or 0 in the request payload
      3. Run: grep -r "openai" DyberPet/ChatPanel/ && echo "FAIL" || echo "OK"
    Expected Result: stream=False in request, no openai import
    Failure Indicators: stream=True, openai import found
    Evidence: .sisyphus/evidence/task-2-no-streaming.txt

  Scenario: Error handling for unreachable endpoint
    Tool: Bash (grep)
    Preconditions: ChatWorker.py is written
    Steps:
      1. Run: grep -n "ConnectError\|TimeoutException\|error_occurred" DyberPet/ChatPanel/ChatWorker.py
      2. Verify at least one error handling path exists
    Expected Result: Error handling for connection failures exists
    Failure Indicators: No error_occurred emit found
    Evidence: .sisyphus/evidence/task-2-error-handling.txt
  ```

  **Evidence to Capture**:
  - [ ] task-2-worker-import.txt
  - [ ] task-2-worker-signals.txt
  - [ ] task-2-no-streaming.txt
  - [ ] task-2-error-handling.txt

  **Commit**: YES
  - Message: `feat(chat): add ChatWorker for LLM API calls`
  - Files: `DyberPet/ChatPanel/__init__.py`, `DyberPet/ChatPanel/ChatWorker.py`, `requirements.txt`
  - Pre-commit: `python -c "from DyberPet.ChatPanel.ChatWorker import ChatWorker; print('OK')"`

- [x] 3. Create ChatPanel UI widget

  **What to do**:
  - Create `DyberPet/ChatPanel/ChatUI.py` with `ChatMainWindow(QWidget)` class
  - The `ChatMainWindow` should follow the `DashboardMainWindow` pattern:
    - QWidget-based (not QDialog)
    - `show_window()` toggle method (show if hidden, hide if visible)
    - Window title with `self.tr('Chat')` for i18n
    - Resizable with minimum size ~350x500
  - Inside ChatMainWindow, create a `ChatPanel(QWidget)` containing:
    - A `QTextEdit` (read-only) for message display (chat history), styled with dark background
    - A `QLineEdit` for message input
    - A `QPushButton` for send
    - Send triggered by button click OR Enter key in QLineEdit
    - A status label showing "Thinking..." when waiting for response
  - Position the window relative to pet screen position on show, but STATIC (don't follow pet movement after opening — like Dashboard)
  - Use `qfluentwidgets` components where available for visual consistency
  - In-memory chat history as a list of `{"role": "user"/"assistant", "content": "..."}` dicts, capped at 100 messages (trim oldest when exceeded)
  - Clear chat history on panel close
  - Disable input field and send button while waiting for LLM response

  **Must NOT do**:
  - Do NOT implement streaming text display
  - Do NOT persist chat history to disk
  - Do NOT add markdown rendering
  - Do NOT make the panel follow pet (static position like Dashboard)
  - Do NOT add model parameters (temperature, etc.)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: []
  - **Skills Evaluated but Omitted**: None — this is purely UI work

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 4, 5
  - **Blocked By**: None (can start immediately)

  **References**:

  **Pattern References** (existing code to follow):
  - `DyberPet/Dashboard/DashboardUI.py:DashboardMainWindow` — Main window class pattern (QWidget, show_window toggle, window flags)
  - `DyberPet/Notification.py:DyberToaster` — For understanding window styling
  - `DyberPet/DyberSettings/DyberControlPanel.py:ControlMainWindow` — Another window pattern with settings

  **API/Type References**:
  - `qfluentwidgets` — Primary UI component library (CardWidget, ScrollArea, LineEdit, PushButton, etc.)

  **WHY Each Reference Matters**:
  - `DashboardMainWindow` is the CLOSEST pattern for the chat window — same QWidget base, same show/hide toggle
  - `ControlMainWindow` shows how to add a settings sub-panel
  - `qfluentwidgets` ensures visual consistency with the rest of the app

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ChatMainWindow imports and is a QWidget subclass
    Tool: Bash
    Preconditions: DyberPet/ChatPanel/ChatUI.py exists
    Steps:
      1. Run: python -c "from PySide6.QtWidgets import QWidget; from DyberPet.ChatPanel.ChatUI import ChatMainWindow; assert issubclass(ChatMainWindow, QWidget); print('OK')"
    Expected Result: ChatMainWindow is importable and subclasses QWidget
    Failure Indicators: ImportError, AttributeError
    Evidence: .sisyphus/evidence/task-3-chatui-import.txt

  Scenario: ChatMainWindow has show_window method
    Tool: Bash
    Preconditions: ChatMainWindow class exists
    Steps:
      1. Run: python -c "from DyberPet.ChatPanel.ChatUI import ChatMainWindow; assert hasattr(ChatMainWindow, 'show_window'); print('OK')"
    Expected Result: show_window method exists (toggle pattern)
    Failure Indicators: AttributeError
    Evidence: .sisyphus/evidence/task-3-show-window.txt

  Scenario: No file I/O for chat history (in-memory only)
    Tool: Bash (grep)
    Preconditions: ChatUI.py is written
    Steps:
      1. Run: grep -r "json.dump\|pickle.dump\|open.*w\|open.*a" DyberPet/ChatPanel/ChatUI.py && echo "FAIL: persistence found" || echo "OK: no persistence"
      2. Run: grep -r "stream.*True\|stream=True" DyberPet/ChatPanel/ChatUI.py && echo "FAIL: streaming found" || echo "OK: no streaming"
    Expected Result: No file writes, no streaming
    Failure Indicators: File I/O or streaming flags found
    Evidence: .sisyphus/evidence/task-3-no-persistence.txt

  Scenario: Chat history has 100-message cap
    Tool: Bash (grep)
    Preconditions: ChatUI.py is written
    Steps:
      1. Run: grep -n "100\|max_messages\|history_cap\|trim\|pop(0)" DyberPet/ChatPanel/ChatUI.py
      2. Verify there's logic to trim older messages when exceeding the cap
    Expected Result: Code exists to cap history at 100 and trim oldest
    Failure Indicators: No cap logic found
    Evidence: .sisyphus/evidence/task-3-history-cap.txt
  ```

  **Evidence to Capture**:
  - [ ] task-3-chatui-import.txt
  - [ ] task-3-show-window.txt
  - [ ] task-3-no-persistence.txt
  - [ ] task-3-history-cap.txt

  **Commit**: YES
  - Message: `feat(chat): add ChatPanel UI widget`
  - Files: `DyberPet/ChatPanel/ChatUI.py`
  - Pre-commit: `python -c "from DyberPet.ChatPanel.ChatUI import ChatMainWindow; print('OK')"`

- [x] 4. Create ChatSettings UI tab

  **What to do**:
  - Create `DyberPet/ChatPanel/ChatSettings.py` with `ChatSettingsTab(QWidget)` class
  - Follow the `BasicSettingUI.py` pattern for settings tabs:
    - Use `qfluentwidgets` `SettingCardGroup` for grouping
    - Create a settings card with LineEdit for `api_url` (default: `http://localhost:18789/v1/`)
    - Create a settings card with LineEdit for `model_name` (default: empty string)
    - Create a settings card withTextEdit (multi-line) for `system_prompt` (default: empty string)
    - Create a SwitchSettingCard for `chat_on` toggle
    - Save settings on change using `settings.save_settings()`
  - Since no `LineEditSettingCard` exists in the project, create a simple one using `SettingCardGroup` with `LineEdit` widgets — keep it minimal, don't over-abstract
  - Use `self.tr()` for all user-visible labels

  **Must NOT do**:
  - Do NOT add temperature, top_p, max_tokens settings
  - Do NOT create a full FluentWindow settings page — just a tab widget
  - Do NOT over-abstract the settings card — keep it simple

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Tasks 1 and 3)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 5
  - **Blocked By**: Tasks 1, 3

  **References**:

  **Pattern References**:
  - `DyberPet/DyberSettings/BasicSettingUI.py` — Settings tab pattern with SettingCardGroup
  - `DyberPet/DyberSettings/BasicSettingUI.py:SwitchSettingCard` — Toggle pattern
  - `DyberPet/DyberSettings/custom_base.py` — Custom widget base patterns

  **API/Type References**:
  - `DyberPet/settings.py:api_url`, `model_name`, `system_prompt`, `chat_on` — The settings globals to bind to

  **WHY Each Reference Matters**:
  - `BasicSettingUI.py` is the EXACT pattern to follow for settings UI
  - `SwitchSettingCard` shows how toggle settings are wired
  - `settings.py` globals are what the UI reads/writes

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ChatSettingsTab imports correctly
    Tool: Bash
    Preconditions: ChatSettings.py exists
    Steps:
      1. Run: python -c "from DyberPet.ChatPanel.ChatSettings import ChatSettingsTab; print('OK')"
    Expected Result: ChatSettingsTab is importable
    Failure Indicators: ImportError
    Evidence: .sisyphus/evidence/task-4-settings-import.txt

  Scenario: Settings UI has fields for all chat settings
    Tool: Bash (grep)
    Preconditions: ChatSettings.py is written
    Steps:
      1. Run: grep -n "api_url\|model_name\|system_prompt\|chat_on" DyberPet/ChatPanel/ChatSettings.py | head -20
      2. Verify all four settings appear in the file with UI bindings
    Expected Result: All four settings have UI elements
    Failure Indicators: Missing settings
    Evidence: .sisyphus/evidence/task-4-settings-fields.txt

  Scenario: URL normalization in settings UI
    Tool: Bash (grep)
    Preconditions: ChatSettings.py is written
    Steps:
      1. Run: grep -n "rstrip\|endswith\|trailing\|normalize\|strip.*/" DyberPet/ChatPanel/ChatSettings.py
      2. Verify there's URL normalization (appending / if missing)
    Expected Result: URL normalization logic exists
    Failure Indicators: No normalization found
    Evidence: .sisyphus/evidence/task-4-url-normalize.txt
  ```

  **Commit**: YES
  - Message: `feat(chat): add ChatSettings UI tab`
  - Files: `DyberPet/ChatPanel/ChatSettings.py`
  - Pre-commit: `python -c "from DyberPet.ChatPanel.ChatSettings import ChatSettingsTab; print('OK')"`

- [x] 5. Wire ChatPanel signals in run_DyberPet.py

  **What to do**:
  - Modify `run_DyberPet.py` to:
    - Add import: `from DyberPet.ChatPanel.ChatUI import ChatMainWindow`
    - In `DyberPetApp.__init__()`, instantiate `self.chat_panel = ChatMainWindow(screens=screens)` (pass screens parameter like Dashboard)
    - In `__connectSignalToSlot()`, wire `self.p.show_chat.connect(self.chat_panel.show_window)`
    - Wire `self.conp.settingInterface` signals for chat settings changes to `self.chat_panel` if needed (settings like chat_on toggle)
  - Modify `DyberPet/DyberPet.py` to:
    - Add `show_chat = Signal(name='show_chat')` to `PetWidget` class (near other signals around line 369)
  - Verify the import chain works: `PetWidget.show_chat` → signal → `DyberPetApp.__connectSignalToSlot` → `ChatMainWindow.show_window`

  **Must NOT do**:
  - Do NOT modify Dashboard or other UI modules
  - Do NOT add streaming signal handling
  - Do NOT change existing signal wiring

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Tasks 1, 2, 3, 4)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 6
  - **Blocked By**: Tasks 1, 2, 3, 4

  **References**:

  **Pattern References**:
  - `run_DyberPet.py:84-152` — `__connectSignalToSlot()` method wiring pattern
  - `run_DyberPet.py:62-75` — Module instantiation pattern (self.p, self.note, self.acc, self.conp, self.board)
  - `DyberPet/DyberPet.py:352-387` — Signal definitions on PetWidget class

  **WHY Each Reference Matters**:
  - These are the EXACT locations to add the import, instantiation, and signal wiring
  - Must follow the identical pattern used for Dashboard and ControlPanel

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: ChatMainWindow is imported and instantiated
    Tool: Bash (grep)
    Preconditions: run_DyberPet.py is modified
    Steps:
      1. Run: grep -n "ChatMainWindow\|chat_panel" run_DyberPet.py
      2. Verify import line and self.chat_panel = ChatMainWindow line exist
    Expected Result: Import and instantiation found
    Failure Indicators: Missing import or instantiation
    Evidence: .sisyphus/evidence/task-5-wiring-import.txt

  Scenario: show_chat signal is wired
    Tool: Bash (grep)
    Preconditions: Both files modified
    Steps:
      1. Run: grep -n "show_chat" run_DyberPet.py DyberPet/DyberPet.py
      2. Verify signal definition in PetWidget and connection in __connectSignalToSlot
    Expected Result: Signal defined and wired
    Failure Indicators: Missing line in either file
    Evidence: .sisyphus/evidence/task-5-signal-wired.txt

  Scenario: Full import chain works
    Tool: Bash
    Preconditions: All modules present
    Steps:
      1. Run: python -c "from DyberPet.DyberPet import PetWidget; assert 'show_chat' in [s for s in dir(PetWidget) if 'chat' in s.lower()]; print('OK')"
    Expected Result: show_chat signal exists on PetWidget
    Failure Indicators: AttributeError
    Evidence: .sisyphus/evidence/task-5-import-chain.txt
  ```

  **Commit**: YES
  - Message: `feat(chat): wire ChatPanel signals in app entry point`
  - Files: `run_DyberPet.py`, `DyberPet/DyberPet.py`
  - Pre-commit: `python -c "from DyberPet.DyberPet import PetWidget; print('OK')"`

- [x] 6. Add Chat menu action to pet right-click menu

  **What to do**:
  - Modify `DyberPet/DyberPet.py` method `_set_Statusmenu()` (around line 882-1014)
  - Add a new `Action` to the right-click menu for "Chat" (or "聊天" with `self.tr()`)
  - Place it after "System" action and before "Select Action" action
  - The action handler should emit `self.show_chat.emit()`
  - Add an appropriate icon using `FIF.CHAT` or `FIF.EMOJI_TAB_SYMBOLS` from qfluentwidgets FluentIcon, or a custom icon if available
  - Verify the menu still renders correctly with the new item

  **Must NOT do**:
  - Do NOT modify other menu actions
  - Do NOT change the menu structure beyond adding the chat action
  - Do NOT add keyboard shortcuts that conflict with existing ones

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 5)
  - **Parallel Group**: Wave 2 (sequential after Task 5)
  - **Blocks**: None (final implementation task)
  - **Blocked By**: Task 5

  **References**:

  **Pattern References**:
  - `DyberPet/DyberPet.py:_set_Statusmenu()` (around line 882) — The method where the right-click menu is built
  - `DyberPet/DyberPet.py:show_dashboard` signal — Pattern for menu action emitting a signal
  - `DyberPet/custom_roundmenu.py` — RoundMenu and Action usage

  **API/Type References**:
  - `qfluentwidgets.FluentIcon` (imported as `FIF`) — Available icons

  **WHY Each Reference Matters**:
  - `_set_Statusmenu()` is the EXACT method to modify
  - `show_dashboard` is the pattern for how menu actions trigger windows
  - `FIF` provides the icon set to choose from

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Chat action exists in status menu method
    Tool: Bash (grep)
    Preconditions: DyberPet.py is modified
    Steps:
      1. Run: grep -n "show_chat\|Chat\|聊天" DyberPet/DyberPet.py | head -20
      2. Verify "show_chat" signal emit is connected to a menu action
      3. Verify the action text includes "Chat" or "聊天"
    Expected Result: Chat menu action with show_chat signal found
    Failure Indicators: No chat-related menu action
    Evidence: .sisyphus/evidence/task-6-menu-action.txt

  Scenario: Menu action emits correct signal
    Tool: Bash (grep)
    Preconditions: DyberPet.py is modified
    Steps:
      1. Run: grep -n "show_chat.emit\|show_chat\.connect" DyberPet/DyberPet.py run_DyberPet.py
      2. Verify signal emission in menu handler and connection in run_DyberPet
    Expected Result: Signal emitted from menu handler, connected to chat_panel.show_window
    Failure Indicators: Missing emit or connect
    Evidence: .sisyphus/evidence/task-6-signal-flow.txt

  Scenario: No other menu actions broken
    Tool: Bash (grep)
    Preconditions: DyberPet.py is modified
    Steps:
      1. Run: grep -n "show_dashboard\|show_controlPanel\|_change_pet\|exit" DyberPet/DyberPet.py | grep -c "Action\|addAction"
      2. Verify existing menu actions are still present (count should be >= 4)
    Expected Result: All original menu actions still exist
    Failure Indicators: Count drops below 4
    Evidence: .sisyphus/evidence/task-6-menu-intact.txt
  ```

  **Commit**: YES
  - Message: `feat(chat): add Chat menu action to pet right-click menu`
  - Files: `DyberPet/DyberPet.py`
  - Pre-commit: `python -c "from DyberPet.DyberPet import PetWidget; print('OK')"`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, grep, import check). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `python -c "from DyberPet.ChatPanel.ChatUI import ChatMainWindow"` to verify imports. Review all changed files for: `as any`, empty except blocks, print statements in production, hardcoded URLs (should use settings), unused imports. Check AI slop: excessive comments, over-abstraction, generic variable names.
  Output: `Imports [PASS/FAIL] | Lint [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill if UI testable)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test: right-click → Chat menu appears, panel opens, message send/receive, settings persist, error handling on offline endpoint, input disabled during wait. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT Have" compliance: no streaming flag, no persistence, no openai SDK, no markdown rendering. Detect cross-task contamination.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **1**: `feat(settings): add chat settings globals (api_url, model_name, system_prompt)` - DyberPet/settings.py
- **2**: `feat(chat): add ChatWorker for LLM API calls` - DyberPet/ChatPanel/ChatWorker.py, DyberPet/ChatPanel/__init__.py, requirements.txt
- **3**: `feat(chat): add ChatPanel UI widget` - DyberPet/ChatPanel/ChatUI.py
- **4**: `feat(chat): add ChatSettings UI tab` - DyberPet/ChatPanel/ChatSettings.py
- **5**: `feat(chat): wire ChatPanel signals in app entry point` - run_DyberPet.py
- **6**: `feat(chat): add Chat menu action to pet right-click menu` - DyberPet/DyberPet.py

---

## Success Criteria

### Verification Commands
```bash
# Module imports successfully
python -c "from DyberPet.ChatPanel.ChatUI import ChatMainWindow; print('OK')"
python -c "from DyberPet.ChatPanel.ChatWorker import ChatWorker; print('OK')"
python -c "from DyberPet.ChatPanel.ChatSettings import ChatSettingsTab; print('OK')"

# Settings globals exist
python -c "import DyberPet.settings as s; s.init(); print(s.api_url, s.model_name)"

# No forbidden patterns
grep -r "stream.*True\|stream=True" DyberPet/ChatPanel/ && echo "FAIL: streaming found" || echo "OK: no streaming"
grep -r "openai" DyberPet/ChatPanel/ && echo "FAIL: openai SDK found" || echo "OK: no openai SDK"
grep -r "json.dump\|pickle.dump" DyberPet/ChatPanel/ && echo "FAIL: persistence found" || echo "OK: no persistence"

# QRunnable pattern used
grep -r "QRunnable" DyberPet/ChatPanel/ChatWorker.py && echo "OK: QRunnable used"

# Signal wiring
grep "show_chat" run_DyberPet.py DyberPet/DyberPet.py && echo "OK: signal wired"
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] Chat panel opens from right-click menu
- [ ] LLM responses display correctly
- [ ] Settings persist across restarts
- [ ] No UI freeze during API calls
- [ ] Error messages show in chat area