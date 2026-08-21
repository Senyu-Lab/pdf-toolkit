from PySide6.QtCore import QByteArray, QSettings


class AppSettings:
    """Manage persistent application settings."""

    def __init__(self):
        self.settings = QSettings(
            "Senyu-Lab",
            "PDF-Toolkit",
        )

    def save_window_geometry(self, geometry: QByteArray):
        """Save the main window geometry."""

        self.settings.setValue(
            "window/geometry",
            geometry,
        )

    def get_window_geometry(self) -> QByteArray | None:
        """Return the saved window geometry."""

        geometry = self.settings.value(
            "window/geometry",
        )

        if isinstance(geometry, QByteArray):
            return geometry

        return None