from PySide6.QtWidgets import QLabel

from gui.main_window import MainWindow


def test_main_window_default_language(
    qtbot,
    app_settings,
):
    window = MainWindow(app_settings)
    qtbot.addWidget(window)

    assert window.language.language == "en"

    qtbot.addWidget(window)

    assert window.language.language == "en"
    assert window.windowTitle() == "PDF Toolkit"

    assert window.merge_button.text() == "Merge PDF"
    assert window.split_button.text() == "Split PDF"
    assert window.delete_button.text() == "Delete Pages"

def test_main_window_switch_to_chinese(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.language.set_language("zh")

    assert window.windowTitle() == "PDF 工具箱"
    assert window.merge_button.text() == "合并 PDF"
    assert window.split_button.text() == "拆分 PDF"
    assert window.delete_button.text() == "删除页面"

def test_main_window_switch_to_japanese(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.language.set_language("ja")

    assert window.windowTitle() == "PDF ツールキット"
    assert window.merge_button.text() == "PDF の結合"
    assert window.split_button.text() == "PDF の分割"
    assert window.delete_button.text() == "ページを削除"

def test_merge_widget_refreshes_with_language(
    qtbot,
    app_settings,
):
    window = MainWindow(app_settings)
    qtbot.addWidget(window)
    qtbot.addWidget(window)

    assert window.merge_widget.title_label.text() == "Merge PDF"

    window.language.set_language("zh")

    assert window.merge_widget.title_label.text() == "合并 PDF"
    assert window.merge_widget.add_button.text() == "添加 PDF"

    window.language.set_language("ja")

    assert window.merge_widget.title_label.text() == "PDF の結合"
    assert window.merge_widget.add_button.text() == "PDF を追加"



def test_language_switch_keeps_merge_state(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)

    pdf_file = tmp_path / "test.pdf"
    output_file = tmp_path / "merged.pdf"

    window.merge_widget.pdf_files = [pdf_file]
    window.merge_widget.output_file = output_file

    window.merge_widget.output_label.setText(
        f"Output: {output_file}"
    )

    window.language.set_language("zh")

    assert window.merge_widget.pdf_files == [pdf_file]
    assert window.merge_widget.output_file == output_file

    window.language.set_language("ja")

    assert window.merge_widget.pdf_files == [pdf_file]
    assert window.merge_widget.output_file == output_file

def test_history_page_is_available(qtbot):
    window = MainWindow()

    qtbot.addWidget(window)

    assert window.pages.indexOf(
        window.history_widget
    ) >= 0

def test_history_refreshes_when_page_is_selected(
    qtbot,
    monkeypatch,
):
    window = MainWindow()

    qtbot.addWidget(window)

    refresh_called = False

    def fake_refresh():
        nonlocal refresh_called
        refresh_called = True

    monkeypatch.setattr(
        window.history_widget,
        "refresh_history",
        fake_refresh,
    )

    history_index = window.pages.indexOf(
        window.history_widget
    )

    window.pages.setCurrentIndex(
        history_index
    )

    assert refresh_called

def test_agent_chat_page_is_available(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.pages.indexOf(
        window.agent_chat_widget
    ) >= 0

    assert window.agent_button is not None

def test_click_agent_button_shows_agent_chat_page(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.agent_button.click()

    assert window.pages.currentWidget() == window.agent_chat_widget

def test_main_window_tracks_current_pdf_path(
    qtbot,
    monkeypatch,
    tmp_path,
):
    window = MainWindow()
    qtbot.addWidget(window)

    pdf_path = tmp_path / "sample.pdf"

    monkeypatch.setattr(
        window.preview_widget,
        "load_pdf",
        lambda path: None,
    )

    assert window.current_pdf_path is None

    window.show_pdf_preview(str(pdf_path))

    assert window.current_pdf_path == str(pdf_path)

def test_main_window_clears_current_pdf_path(
    qtbot,
    monkeypatch,
    tmp_path,
):
    window = MainWindow()
    qtbot.addWidget(window)

    pdf_path = tmp_path / "sample.pdf"

    monkeypatch.setattr(
        window.preview_widget,
        "load_pdf",
        lambda path: None,
    )
    monkeypatch.setattr(
        window.preview_widget,
        "close_document",
        lambda: None,
    )

    window.show_pdf_preview(str(pdf_path))
    assert window.current_pdf_path == str(pdf_path)

    window.show_pdf_preview(None)

    assert window.current_pdf_path is None

def test_main_window_sends_question_to_agent_service(
    qtbot,
    monkeypatch,
    tmp_path,
):
    from unittest.mock import Mock

    window = MainWindow()
    qtbot.addWidget(window)

    pdf_path = tmp_path / "sample.pdf"
    question = "请总结这份 PDF"
    answer = "这份 PDF 主要介绍了数据分析方法。"

    service = Mock()
    service.ask.return_value = answer
    window.agent_service = service

    monkeypatch.setattr(
        window.preview_widget,
        "load_pdf",
        lambda path: None,
    )

    window.show_pdf_preview(str(pdf_path))

    window.agent_chat_widget.message_submitted.emit(question)

    service.ask.assert_called_once_with(str(pdf_path), question)

    bubbles = window.agent_chat_widget.findChildren(
        QLabel,
        "assistantMessageBubble",
    )
    assert any(bubble.text() == answer for bubble in bubbles)

def test_main_window_prompts_when_no_pdf_is_selected(
    qtbot,
):
    from unittest.mock import Mock

    window = MainWindow()
    qtbot.addWidget(window)

    service = Mock()
    window.agent_service = service

    window.agent_chat_widget.message_submitted.emit(
        "请总结这份 PDF"
    )

    service.ask.assert_not_called()

    bubbles = window.agent_chat_widget.findChildren(
        QLabel,
        "assistantMessageBubble",
    )

    assert any(
        bubble.text() == "Please select a PDF file first."
        for bubble in bubbles
    )

def test_main_window_displays_error_when_agent_fails(
    qtbot,
    monkeypatch,
    tmp_path,
):
    from unittest.mock import Mock

    window = MainWindow()
    qtbot.addWidget(window)

    pdf_path = tmp_path / "sample.pdf"

    monkeypatch.setattr(
        window.preview_widget,
        "load_pdf",
        lambda path: None,
    )

    window.show_pdf_preview(str(pdf_path))

    service = Mock()
    service.ask.side_effect = RuntimeError(
        "Agent execution failed"
    )
    window.agent_service = service

    window.agent_chat_widget.message_submitted.emit(
        "请总结这份 PDF"
    )

    service.ask.assert_called_once_with(
        str(pdf_path),
        "请总结这份 PDF",
    )

    bubbles = window.agent_chat_widget.findChildren(
        QLabel,
        "assistantMessageBubble",
    )

    assert any(
        bubble.text()
        == "Sorry, I couldn't process your question."
        for bubble in bubbles
    )

def test_main_window_accepts_injected_agent_service(
    qtbot,
):
    from unittest.mock import Mock

    from gui.main_window import MainWindow

    agent_service = Mock()

    window = MainWindow(
        agent_service=agent_service,
    )
    qtbot.addWidget(window)

    assert window.agent_service is agent_service