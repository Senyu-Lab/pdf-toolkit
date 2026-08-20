import pytest

from gui.i18n import LanguageManager


def test_default_language():
    manager = LanguageManager()

    assert manager.language == "en"
    assert manager.get("app.title") == "PDF Toolkit"


def test_switch_to_chinese():
    manager = LanguageManager()

    manager.set_language("zh")

    assert manager.language == "zh"
    assert manager.get("app.title") == "PDF 工具箱"


def test_switch_to_japanese():
    manager = LanguageManager()

    manager.set_language("ja")

    assert manager.language == "ja"
    assert manager.get("app.title") == "PDF ツールキット"


def test_unknown_key_returns_key():
    manager = LanguageManager()

    assert manager.get("unknown.key") == "unknown.key"


def test_invalid_language():
    manager = LanguageManager()

    with pytest.raises(ValueError):
        manager.set_language("fr")

def test_language_changed_signal(qtbot):
    manager = LanguageManager()

    received_languages = []

    manager.language_changed.connect(
        received_languages.append
    )

    manager.set_language("zh")

    assert received_languages == ["zh"]

def test_language_changed_signal_not_emitted_for_same_language(qtbot):
    manager = LanguageManager()

    received_languages = []

    manager.language_changed.connect(
        received_languages.append
    )

    manager.set_language("en")

    assert received_languages == []