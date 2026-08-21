from PySide6.QtCore import QObject, Signal

from gui.i18n.translations import TRANSLATIONS


class LanguageManager(QObject):

    language_changed = Signal(str)

    def __init__(self, language: str = "en"):
        super().__init__()

        if language not in TRANSLATIONS:
            raise ValueError(f"Unsupported language: {language}")

        self.language = language

    def get(self, key: str) -> str:

        return TRANSLATIONS[self.language].get(key, key)

    def set_language(self, language: str):

        if language not in TRANSLATIONS:
            raise ValueError(f"Unsupported language: {language}")

        if language == self.language:
            return

        self.language = language
        self.language_changed.emit(language)