APP_STYLE = """
QMainWindow {
    background-color: #f5f7fa;
}

QWidget {
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 14px;
    color: #2c3e50;
}

QLabel#pageTitle {
    font-size: 24px;
    font-weight: 600;
    color: #1f2937;
    padding-bottom: 8px;
}

QLabel#sectionTitle {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
}

QPushButton {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 16px;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #f3f4f6;
    border-color: #9ca3af;
}

QPushButton:pressed {
    background-color: #e5e7eb;
}

QPushButton#primaryButton {
    background-color: #2563eb;
    color: white;
    border: none;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #1d4ed8;
}

QPushButton#primaryButton:pressed {
    background-color: #1e40af;
}

QPushButton#dangerButton {
    background-color: #ffffff;
    color: #dc2626;
    border: 1px solid #fecaca;
}

QPushButton#dangerButton:hover {
    background-color: #fef2f2;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 6px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 5px;
}

QListWidget::item:selected {
    background-color: #dbeafe;
    color: #1e40af;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px;
}

QLineEdit:focus {
    border: 1px solid #2563eb;
}

QLabel#outputLabel {
    color: #6b7280;
    padding: 6px;
}

QStatusBar {
    color: #6b7280;
}
"""