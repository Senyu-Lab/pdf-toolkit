from PySide6.QtCore import QByteArray, QSettings


# Manage persistent application settings.
class AppSettings:
    def __init__(self, settings: QSettings | None = None):
        self.settings = settings or QSettings(
            "Senyu-Lab",
            "PDF-Toolkit",
        )

    # Save the main window geometry.
    def save_window_geometry(self, geometry: QByteArray):

        self.settings.setValue(
            "window/geometry",
            geometry,
        )

    # Return the saved window geometry.
    def get_window_geometry(self) -> QByteArray | None:

        geometry = self.settings.value(
            "window/geometry",
        )

        if isinstance(geometry, QByteArray):
            return geometry

        return None

    def save_language(self, language: str):
        self.settings.setValue(
            "language",
            language,
        )

    def get_language(self) -> str:
        language = self.settings.value(
            "language",
            "en",
        )

        return language