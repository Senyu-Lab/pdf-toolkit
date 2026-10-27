
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class AgentChatWidget(QWidget):
    # Notify the caller when the user submits a message.
    message_submitted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.message_view = QTextEdit()
        self.message_view.setReadOnly(True)
        self.message_view.setPlaceholderText(
            "Your conversation will appear here."
        )

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(
            "Ask a question about your PDF..."
        )
        self.input_edit.setMaximumHeight(120)

        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("primaryButton")
        self.send_button.clicked.connect(
            self._send_message
        )

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.send_button)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("AI Assistant"))
        layout.addWidget(self.message_view)
        layout.addLayout(input_layout)

    def add_message(self, role: str, message: str):
        # Display each message with a readable speaker label.
        if role == "user":
            speaker = "You"
        elif role == "assistant":
            speaker = "AI Assistant"
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
