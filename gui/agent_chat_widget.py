
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
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

        self.message_scroll_area = QScrollArea()
        self.message_scroll_area.setWidgetResizable(True)

        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.message_layout.setSpacing(12)

        self.empty_state_label = QLabel()
        self.empty_state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.message_layout.addWidget(self.empty_state_label)

        self.message_scroll_area.setWidget(self.message_container)

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
        layout.addWidget(self.message_scroll_area)
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
        self.empty_state_label.setText(
            self.language.get("agent.conversation_placeholder")
        )
        self.input_edit.setPlaceholderText(
            self.language.get("agent.input_placeholder")
        )

    def add_message(self, role: str, message: str):
        if role == "user":
            bubble_name = "userMessageBubble"
            bubble_color = "#D9FDD3"
            alignment = Qt.AlignmentFlag.AlignRight
        elif role == "assistant":
            bubble_name = "assistantMessageBubble"
            bubble_color = "#F1F1F1"
            alignment = Qt.AlignmentFlag.AlignLeft
        else:
            raise ValueError(f"Unsupported message role: {role}")

        self.empty_state_label.hide()

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        bubble = QLabel(message)
        bubble.setObjectName(bubble_name)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        bubble.setMaximumWidth(500)
        bubble.setStyleSheet(
            f"""
            QLabel {{
                background-color: {bubble_color};
                color: #222222;
                border-radius: 10px;
                padding: 8px 12px;
            }}
            """
        )

        if role == "user":
            row_layout.addStretch()
            row_layout.addWidget(bubble, 0, alignment)
        else:
            row_layout.addWidget(bubble, 0, alignment)
            row_layout.addStretch()

        self.message_layout.addWidget(row)

        self.message_scroll_area.verticalScrollBar().setValue(
            self.message_scroll_area.verticalScrollBar().maximum()
        )

    def _send_message(self):
        message = self.input_edit.toPlainText().strip()

        if not message:
            return

        self.add_message("user", message)
        self.message_submitted.emit(message)
        self.input_edit.clear()
