
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

    assert "Summarize this PDF" in widget.message_view.toPlainText()
    assert "Here is the summary." in widget.message_view.toPlainText()

def test_send_message_adds_user_message_to_history(qtbot):
    widget = AgentChatWidget()
    qtbot.addWidget(widget)

    widget.input_edit.setPlainText("Summarize this PDF")
    widget.send_button.click()

    assert "You: Summarize this PDF" in widget.message_view.toPlainText()




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
    assert "你: 你好" in widget.message_view.toPlainText()

    language.set_language("ja")
    widget.refresh_ui()

    assert widget.title_label.text() == "AI アシスタント"
    assert widget.send_button.text() == "送信"
