# coding:utf-8
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from qfluentwidgets import (
    PushButton, LineEdit, CaptionLabel,
    FluentIcon as FIF, isDarkTheme,
)

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
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(self.tr("Chat"))
        self.setMinimumSize(350, 500)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.chat_panel = ChatPanel(self)
        layout.addWidget(self.chat_panel)

    def show_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def closeEvent(self, event):
        self.chat_panel.clear_history()
        event.ignore()
        self.hide()