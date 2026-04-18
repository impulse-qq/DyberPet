# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit

from qfluentwidgets import (
    SettingCardGroup, SwitchSettingCard, ExpandLayout,
    FluentIcon as FIF, TextEdit, ScrollArea, SettingCard,
)

import DyberPet.settings as settings


class _LineEditSettingCard(SettingCard):
    """Simple setting card with a LineEdit for text input."""

    def __init__(self, icon, title, content, echo_mode=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(260)
        self.lineEdit.setClearButtonEnabled(True)
        if echo_mode:
            self.lineEdit.setEchoMode(echo_mode)
        self.hBoxLayout.addWidget(self.lineEdit)
        self.hBoxLayout.addSpacing(16)


class _TextEditSettingCard(SettingCard):
    """Simple setting card with a multi-line TextEdit for longer text input."""

    def __init__(self, icon, title, content, parent=None):
        super().__init__(icon, title, content, parent)
        self.textEdit = TextEdit(self)
        self.textEdit.setFixedHeight(80)
        self.textEdit.setPlaceholderText(content)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(48, 0, 16, 16)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.textEdit)


class ChatSettingsTab(ScrollArea):
    """Chat settings tab widget."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ChatSettingsTab")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # Header label
        self.settingLabel = QLabel(self.tr("Chat Settings"), self)

        # API Settings group
        self.apiGroup = SettingCardGroup(self.tr('API'), self.scrollWidget)

        self.apiUrlCard = _LineEditSettingCard(
            FIF.LINK,
            self.tr("API URL"),
            self.tr("OpenAI-compatible API endpoint"),
            parent=self.apiGroup
        )
        self.apiUrlCard.lineEdit.setText(settings.api_url)
        self.apiUrlCard.lineEdit.editingFinished.connect(self._ApiUrlChanged)

        self.modelNameCard = _LineEditSettingCard(
            FIF.ROBOT,
            self.tr("Model Name"),
            self.tr("Model identifier for the chat API"),
            parent=self.apiGroup
        )
        self.modelNameCard.lineEdit.setText(settings.model_name)
        self.modelNameCard.lineEdit.editingFinished.connect(self._ModelNameChanged)

        self.apiKeyCard = _LineEditSettingCard(
            FIF.FLAG,
            self.tr("API Key"),
            self.tr("Optional: leave empty for local LLMs"),
            echo_mode=QLineEdit.EchoMode.Password,
            parent=self.apiGroup
        )
        self.apiKeyCard.lineEdit.setText(settings.api_key)
        self.apiKeyCard.lineEdit.editingFinished.connect(self._ApiKeyChanged)

        # Prompt Settings group
        self.promptGroup = SettingCardGroup(self.tr('Prompt'), self.scrollWidget)

        self.systemPromptCard = _TextEditSettingCard(
            FIF.EDIT,
            self.tr("System Prompt"),
            self.tr("System prompt sent with each message"),
            parent=self.promptGroup
        )
        self.systemPromptCard.textEdit.setPlainText(settings.system_prompt)
        self.systemPromptCard.textEdit.textChanged.connect(self._SystemPromptChanged)

        # Chat Toggle group
        self.chatGroup = SettingCardGroup(self.tr('Chat'), self.scrollWidget)

        self.chatOnCard = SwitchSettingCard(
            FIF.CHAT,
            self.tr("Enable Chat"),
            self.tr("Turn on/off the chat panel"),
            parent=self.chatGroup
        )
        if settings.chat_on:
            self.chatOnCard.setChecked(True)
        else:
            self.chatOnCard.setChecked(False)
        self.chatOnCard.switchButton.checkedChanged.connect(self._ChatOnChanged)

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 75, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.__initLayout()

    def __initLayout(self):
        self.settingLabel.move(50, 20)

        # Add cards to groups
        self.apiGroup.addSettingCard(self.apiUrlCard)
        self.apiGroup.addSettingCard(self.modelNameCard)
        self.apiGroup.addSettingCard(self.apiKeyCard)

        self.promptGroup.addSettingCard(self.systemPromptCard)

        self.chatGroup.addSettingCard(self.chatOnCard)

        # Add groups to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)

        self.expandLayout.addWidget(self.apiGroup)
        self.expandLayout.addWidget(self.promptGroup)
        self.expandLayout.addWidget(self.chatGroup)

    def _ApiUrlChanged(self):
        url = self.apiUrlCard.lineEdit.text().strip()
        if url and not url.endswith('/'):
            url += '/'
        settings.api_url = url
        settings.save_settings()

    def _ModelNameChanged(self):
        settings.model_name = self.modelNameCard.lineEdit.text().strip()
        settings.save_settings()

    def _ApiKeyChanged(self):
        settings.api_key = self.apiKeyCard.lineEdit.text().strip()
        settings.save_settings()

    def _SystemPromptChanged(self):
        settings.system_prompt = self.systemPromptCard.textEdit.toPlainText()
        settings.save_settings()

    def _ChatOnChanged(self, isChecked):
        if isChecked:
            settings.chat_on = True
        else:
            settings.chat_on = False
        settings.save_settings()