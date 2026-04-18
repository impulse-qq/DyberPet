# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit,
)
from qfluentwidgets import (
    SettingCardGroup, SwitchSettingCard, ExpandLayout,
    FluentIcon as FIF, ScrollArea, SettingCard,
)

import DyberPet.settings as settings


class _PromptSettingCard(SettingCard):
    """SettingCard with a QTextEdit below the title row."""

    def __init__(self, icon, title, desc, parent=None):
        super().__init__(icon, title, desc, parent)
        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedHeight(80)
        self.text_edit.setPlaceholderText(desc)

        self.hBoxLayout.addSpacing(16)

        self._text_layout = QVBoxLayout()
        self._text_layout.setContentsMargins(48, 0, 16, 12)
        self._text_layout.addWidget(self.text_edit)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addLayout(self.hBoxLayout)
        outer.addLayout(self._text_layout)


class ChatSettingsTab(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ChatSettingsTab")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # API Settings group
        self.apiGroup = SettingCardGroup(self.tr('API'), self.scrollWidget)

        self.apiUrlCard = self._make_line_edit_card(
            FIF.LINK, self.tr("API URL"),
            self.tr("OpenAI-compatible API endpoint"),
            self.apiGroup
        )
        self.apiUrlCard.lineEdit.setText(settings.api_url)
        self.apiUrlCard.lineEdit.editingFinished.connect(self._ApiUrlChanged)

        self.modelNameCard = self._make_line_edit_card(
            FIF.ROBOT, self.tr("Model Name"),
            self.tr("e.g. openclaw/default"),
            self.apiGroup
        )
        self.modelNameCard.lineEdit.setText(settings.model_name)
        self.modelNameCard.lineEdit.editingFinished.connect(self._ModelNameChanged)

        self.apiKeyCard = self._make_line_edit_card(
            FIF.FLAG, self.tr("API Key"),
            self.tr("Optional: leave empty for local LLMs"),
            self.apiGroup,
            echo_mode=QLineEdit.EchoMode.Password
        )
        self.apiKeyCard.lineEdit.setText(settings.api_key)
        self.apiKeyCard.lineEdit.editingFinished.connect(self._ApiKeyChanged)

        # Display Settings group
        self.displayGroup = SettingCardGroup(self.tr('Display'), self.scrollWidget)

        self.petNameCard = self._make_line_edit_card(
            FIF.PEOPLE, self.tr("Pet Name"),
            self.tr("Name shown for the pet in chat (default: uses character name)"),
            self.displayGroup
        )
        self.petNameCard.lineEdit.setText(settings.chat_pet_name)
        self.petNameCard.lineEdit.editingFinished.connect(self._PetNameChanged)

        # Prompt Settings group
        self.promptGroup = SettingCardGroup(self.tr('Prompt'), self.scrollWidget)

        self.systemPromptCard = _PromptSettingCard(
            FIF.EDIT, self.tr("System Prompt"),
            self.tr("System prompt sent with each message"),
            self.promptGroup
        )
        self.systemPromptCard.text_edit.setPlainText(settings.system_prompt)
        self.systemPromptCard.text_edit.textChanged.connect(self._SystemPromptChanged)

        # Chat Toggle group
        self.chatGroup = SettingCardGroup(self.tr('Chat'), self.scrollWidget)

        self.chatOnCard = SwitchSettingCard(
            FIF.CHAT,
            self.tr("Enable Chat"),
            self.tr("Turn on/off the chat panel"),
            parent=self.chatGroup
        )
        self.chatOnCard.setChecked(settings.chat_on)
        self.chatOnCard.switchButton.checkedChanged.connect(self._ChatOnChanged)

        self.__initWidget()

    # -- factory helpers --

    @staticmethod
    def _make_line_edit_card(icon, title, desc, parent, echo_mode=None):
        card = SettingCard(icon, title, desc, parent)
        card.lineEdit = QLineEdit(card)
        card.lineEdit.setFixedWidth(260)
        card.lineEdit.setClearButtonEnabled(True)
        if echo_mode is not None:
            card.lineEdit.setEchoMode(echo_mode)
        card.hBoxLayout.addWidget(card.lineEdit)
        card.hBoxLayout.addSpacing(16)
        return card

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 10, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.__initLayout()

    def __initLayout(self):
        # Add cards to groups
        self.apiGroup.addSettingCard(self.apiUrlCard)
        self.apiGroup.addSettingCard(self.modelNameCard)
        self.apiGroup.addSettingCard(self.apiKeyCard)

        self.displayGroup.addSettingCard(self.petNameCard)

        self.promptGroup.addSettingCard(self.systemPromptCard)

        self.chatGroup.addSettingCard(self.chatOnCard)

        # Add groups to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)

        self.expandLayout.addWidget(self.apiGroup)
        self.expandLayout.addWidget(self.displayGroup)
        self.expandLayout.addWidget(self.promptGroup)
        self.expandLayout.addWidget(self.chatGroup)

    # -- change handlers --

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

    def _PetNameChanged(self):
        settings.chat_pet_name = self.petNameCard.lineEdit.text().strip()
        settings.save_settings()

    def _SystemPromptChanged(self):
        settings.system_prompt = self.systemPromptCard.text_edit.toPlainText()
        settings.save_settings()

    def _ChatOnChanged(self, isChecked):
        settings.chat_on = isChecked
        settings.save_settings()