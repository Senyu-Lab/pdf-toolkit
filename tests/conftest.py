import pytest
from PySide6.QtCore import QSettings

from gui.settings import AppSettings


@pytest.fixture
def app_settings(tmp_path):
    settings = QSettings(
        str(tmp_path / "settings.ini"),
        QSettings.IniFormat,
    )

    settings.setValue("language", "en")

    return AppSettings(settings)