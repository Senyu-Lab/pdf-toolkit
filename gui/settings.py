from PySide6.QtCore import QByteArray, QSettings


# Manage persistent application settings.
class AppSettings:

    def __init__(self):
        self.settings = QSettings(
            "Senyu-Lab",
            "PDF-Toolkit",
        )

    # Save the main window geometry.
    def save_window_geometry(self, geometry: QByteArray):

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