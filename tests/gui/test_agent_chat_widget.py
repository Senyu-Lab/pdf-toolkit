from PySide6.QtWidgets import QLabel

from gui.agent_chat_widget import AgentChatWidget
from gui.i18n.manager import LanguageManager


def test_send_message_emits_signal_and_clears_input(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    with qtbot.waitSignal(
        widget.message_submitted,
        timeout=1000,
    ) as signal:
        widget.input_edit.setPlainText("Summarize this PDF")
        widget.send_button.click()

    assert signal.args == ["Summarize this PDF"]
    assert widget.input_edit.toPlainText() == ""


def test_add_message_displays_user_and_assistant_messages(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    widget.add_message("user", "Summarize this PDF")
    widget.add_message("assistant", "Here is the summary.")

    user_bubble = widget.findChild(
        QLabel,
        "userMessageBubble",
    )
    assistant_bubble = widget.findChild(
        QLabel,
        "assistantMessageBubble",
    )

    assert user_bubble.text() == "Summarize this PDF"
    assert assistant_bubble.text() == "Here is the summary."

def test_send_message_adds_user_message_to_history(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    widget.input_edit.setPlainText("Summarize this PDF")
    widget.send_button.click()

    user_bubble = widget.findChild(
        QLabel,
        "userMessageBubble",
    )

    assert user_bubble is not None
    assert user_bubble.text() == "Summarize this PDF"




def test_agent_chat_widget_uses_translations(qtbot):
    language = LanguageManager("zh")
    widget = AgentChatWidget(language=language)
    qtbot.addWidget(widget)

    assert widget.title_label.text() == "AI 助手"
    assert widget.send_button.text() == "发送"
    assert widget.input_edit.placeholderText() == (
        "请输入关于 PDF 的问题……"
    )

    widget.add_message("user", "你好")
    user_bubble = widget.findChild(
        QLabel,
        "userMessageBubble",
    )

    assert user_bubble is not None
    assert user_bubble.text() == "你好"

    language.set_language("ja")
    widget.refresh_ui()

    assert widget.title_label.text() == "AI アシスタント"
    assert widget.send_button.text() == "送信"

def test_add_message_creates_separate_bubbles(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    widget.add_message("user", "Hello")
    widget.add_message("assistant", "Hi there")

    user_bubble = widget.findChild(
        QLabel,
        "userMessageBubble",
    )
    assistant_bubble = widget.findChild(
        QLabel,
        "assistantMessageBubble",
    )

    assert user_bubble is not None
    assert assistant_bubble is not None
    assert user_bubble.text() == "Hello"
    assert assistant_bubble.text() == "Hi there"

def test_message_bubbles_are_aligned_by_role(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    widget.add_message("user", "Hello")
    widget.add_message("assistant", "Hi")

    user_bubble = widget.findChild(
        QLabel,
        "userMessageBubble",
    )
    assistant_bubble = widget.findChild(
        QLabel,
        "assistantMessageBubble",
    )

    user_row = user_bubble.parentWidget()
    assistant_row = assistant_bubble.parentWidget()

    user_layout = user_row.layout()
    assistant_layout = assistant_row.layout()

    assert user_layout.itemAt(0).spacerItem() is not None
    assert assistant_layout.itemAt(
        assistant_layout.count() - 1
    ).spacerItem() is not None