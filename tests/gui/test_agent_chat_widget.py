
from gui.agent_chat_widget import AgentChatWidget


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

    assert "Summarize this PDF" in widget.message_view.toPlainText()
    assert "Here is the summary." in widget.message_view.toPlainText()

def test_send_message_adds_user_message_to_history(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    widget.input_edit.setPlainText("Summarize this PDF")
    widget.send_button.click()

    assert "You: Summarize this PDF" in widget.message_view.toPlainText()