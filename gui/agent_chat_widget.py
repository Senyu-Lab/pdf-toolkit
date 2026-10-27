
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gui.i18n.manager import LanguageManager


class AgentChatWidget(QWidget):
    # Notify the caller when the user submits a message.
    message_submitted = Signal(str)

    def __init__(self, language=None, parent=None):
        super().__init__(parent)

        # Use English when no language manager is provided.
        self.language = language or LanguageManager("en")

        self.title_label = QLabel()

        self.message_view = QTextEdit()
        self.message_view.setReadOnly(True)

        self.input_edit = QTextEdit()
        self.input_edit.setMaximumHeight(120)

        self.send_button = QPushButton()
        self.send_button.setObjectName("primaryButton")
        self.send_button.clicked.connect(self._send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.send_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_view)
        layout.addLayout(input_layout)

        # Apply the initial language after all widgets are created.
        self.refresh_ui()

    def refresh_ui(self):
        # Refresh visible text when the application language changes.
        self.title_label.setText(
            self.language.get("agent.title")
        )
        self.send_button.setText(
            self.language.get("agent.send")
        )
        self.message_view.setPlaceholderText(
            self.language.get("agent.conversation_placeholder")
        )
        self.input_edit.setPlaceholderText(
            self.language.get("agent.input_placeholder")
        )

    def add_message(self, role: str, message: str):
        if role == "user":
            speaker = self.language.get("agent.user")
        elif role == "assistant":
            speaker = self.language.get("agent.assistant")
        else:
            raise ValueError(f"Unsupported message role: {role}")

        self.message_view.append(f"{speaker}: {message}")

    def _send_message(self):
        message = self.input_edit.toPlainText().strip()

        if not message:
            return

        self.add_message("user", message)
        self.message_submitted.emit(message)
        self.input_edit.clear()
