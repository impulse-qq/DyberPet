# coding:utf-8
from PySide6.QtCore import Qt, Signal, QThreadPool
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from qfluentwidgets import (
    PushButton, LineEdit, CaptionLabel,
    FluentIcon as FIF, isDarkTheme,
)

import DyberPet.settings as settings
from DyberPet.ChatPanel.ChatWorker import ChatWorker

MAX_CHAT_HISTORY = 100


class ChatPanel(QWidget):

    message_sent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_history: list[dict[str, str]] = []
        self._input_enabled = True
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._apply_display_style()
        layout.addWidget(self.message_display, stretch=1)

        self.status_label = CaptionLabel(self.tr("Ready"))
        layout.addWidget(self.status_label)

        input_row = QHBoxLayout()
        input_row.setSpacing(6)

        self.input_field = LineEdit()
        self.input_field.setPlaceholderText(self.tr("Type a message..."))
        self.input_field.setClearButtonEnabled(True)
        self.input_field.returnPressed.connect(self._on_send)
        input_row.addWidget(self.input_field, stretch=1)

        self.send_button = PushButton(FIF.SEND, self.tr("Send"))
        self.send_button.clicked.connect(self._on_send)
        input_row.addWidget(self.send_button)

        layout.addLayout(input_row)

    def _apply_display_style(self):
        dark = isDarkTheme()
        bg = "#1e1e1e" if dark else "#f5f5f5"
        fg = "#e0e0e0" if dark else "#1a1a1a"
        self.message_display.setStyleSheet(
            f"QTextEdit {{ background-color: {bg}; color: {fg}; "
            f"border: 1px solid {'#3a3a3a' if dark else '#d0d0d0'}; "
            f"border-radius: 6px; padding: 6px; }}"
        )

    def _on_send(self):
        text = self.input_field.text().strip()
        if not text or not self._input_enabled:
            return
        self.input_field.clear()
        self.add_message("user", text)
        self.message_sent.emit(text)

    def add_message(self, role: str, content: str):
        self.chat_history.append({"role": role, "content": content})
        while len(self.chat_history) > MAX_CHAT_HISTORY:
            self.chat_history.pop(0)

        prefix = self.tr("You") if role == "user" else self.tr("Pet")
        self.message_display.append(f"<b>{prefix}:</b> {content}")
        self.message_display.moveCursor(QTextCursor.MoveOperation.End)

    def clear_history(self):
        self.chat_history.clear()
        self.message_display.clear()

    def set_input_enabled(self, enabled: bool):
        self._input_enabled = enabled
        self.input_field.setEnabled(enabled)
        self.send_button.setEnabled(enabled)

    def set_status(self, text: str):
        self.status_label.setText(text)


class ChatMainWindow(QWidget):

    def __init__(self, screens=None):
        super().__init__()
        self.screens = screens
        self._thread_pool = QThreadPool()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(self.tr("Chat"))
        self.setMinimumSize(350, 500)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowTitleHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.chat_panel = ChatPanel(self)
        layout.addWidget(self.chat_panel)

        # Connect chat panel signals
        self.chat_panel.message_sent.connect(self._on_message_sent)

    def _on_message_sent(self, text: str):
        """Handle user sending a message: call LLM API."""
        if not settings.chat_on:
            self.chat_panel.add_message("system", self.tr("Chat is disabled. Enable it in settings."))
            return

        api_url = settings.api_url
        model_name = settings.model_name
        api_key = settings.api_key
        system_prompt = settings.system_prompt

        # Build messages list with optional system prompt
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(self.chat_panel.chat_history)

        # Disable input while waiting
        self.chat_panel.set_input_enabled(False)
        self.chat_panel.set_status(self.tr("Thinking..."))

        # Create and start worker
        worker = ChatWorker(messages, api_url, model_name, api_key)
        worker.signals.response_received.connect(self._on_response_received)
        worker.signals.error_occurred.connect(self._on_error_occurred)
        self._thread_pool.start(worker)

    def _on_response_received(self, content: str):
        """Handle successful LLM response."""
        self.chat_panel.add_message("assistant", content)
        self.chat_panel.set_input_enabled(True)
        self.chat_panel.set_status(self.tr("Ready"))

    def _on_error_occurred(self, error_msg: str):
        """Handle LLM API error."""
        self.chat_panel.add_message("system", f"Error: {error_msg}")
        self.chat_panel.set_input_enabled(True)
        self.chat_panel.set_status(self.tr("Error"))

    def show_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def closeEvent(self, event):
        self.chat_panel.clear_history()
        event.ignore()
        self.hide()