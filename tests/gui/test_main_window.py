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