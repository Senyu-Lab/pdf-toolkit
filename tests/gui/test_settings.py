from PySide6.QtCore import QByteArray

from gui.settings import AppSettings


def test_save_and_get_window_geometry(qapp, monkeypatch):
    settings = AppSettings()
    geometry = QByteArray(b"test-geometry")

    settings.settings.clear()

    settings.save_window_geometry(geometry)

    assert settings.get_window_geometry() == geometry


def test_get_window_geometry_without_saved_value(qapp):
    settings = AppSettings()

    settings.settings.clear()

    assert settings.get_window_geometry() is None


def test_get_window_geometry_with_invalid_type(qapp):
    settings = AppSettings()

    settings.settings.clear()
    settings.settings.setValue(
        "window/geometry",
        "invalid-geometry",
    )

    assert settings.get_window_geometry() is None

def test_save_and_get_language(qapp):
    settings = AppSettings()

    settings.settings.clear()

    settings.save_language("zh")

    assert settings.get_language() == "zh"

def test_get_language_without_saved_value(qapp):
    settings = AppSettings()

    settings.settings.clear()

    assert settings.get_language() == "en"