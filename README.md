# PDF Toolkit

[![CI](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml)

A simple Python tool for merging, splitting, and editing PDF files.

PDF Toolkit provides both a command-line interface (CLI) and a graphical user interface (GUI) built with PySide6.

## Features

* Merge multiple PDF files into one PDF
* Split a PDF by page ranges
* Delete specific pages or page ranges from a PDF
* Support multiple page ranges
* Validate user input and page ranges
* Drag and drop PDF files
* Reorder PDF files by drag and drop when merging
* Command-line interface (CLI)
* Graphical user interface (GUI) built with PySide6
* Multilingual GUI support

  * English
  * 中文
  * 日本語
* Windows executable release

## Requirements

* Python 3.10+
* PyMuPDF
* PySide6
* pytest
* pytest-qt
* Ruff
* PyInstaller

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Senyu-Lab/pdf-toolkit.git
cd pdf-toolkit
pip install -r requirements.txt
```

## Usage

PDF Toolkit provides both a command-line interface and a graphical user interface.

### CLI

Put PDF files into the `input` folder.

Run:

```bash
python main.py
```

Then choose an option from the menu.

### GUI

Run:

```bash
python gui_main.py
```

The GUI currently provides the following operations:

* Merge PDF
* Split PDF
* Delete PDF pages

The GUI also supports PDF file drag and drop.

## Multilingual Support

The GUI currently supports three languages:

* English
* 中文
* 日本語

The internationalization system is separated from the core PDF processing logic.

Translation resources are located in:

```text
gui/
└── i18n/
    ├── __init__.py
    ├── manager.py
    └── translations.py
```

The language manager provides a centralized way to manage translated interface text.

Additional languages can be added by extending the translation resources without changing the core PDF processing logic.

## Database

The project uses SQLite for local data persistence and is currently
developing the foundation for operation history.

The database layer is separated from the GUI and PDF processing logic.
SQL statements are maintained separately from Python code to keep the
database layer modular and maintainable.

The current database layer provides:

- SQLite database initialization
- Database connection management
- Operation history repository
- Insert operations
- Query operations
- Delete operations
- Clear operations
- Input validation
- Automated database tests

## Windows Executable

A pre-built Windows x64 executable is available from the GitHub Releases page.

### Download

Download the latest release:

**v1.1.0**

Download:

```text
PDF-Toolkit-Windows-x64.zip
```

After downloading, extract the ZIP file and run:

```text
PDF-Toolkit.exe
```

The packaged Windows version does not require Python to be installed.

## Merge PDFs

Select:

```text
1. Merge PDFs
```

The PDF files in the input directory will be merged into the specified output file.

For example:

```text
output/merged.pdf
```

### GUI Merge

In the GUI, PDF files can be added through the file selection dialog or by dragging PDF files into the file list.

The order of PDF files can also be changed by dragging them within the list.

Duplicate PDF files are automatically prevented.

## Split PDF

Select:

```text
2. Split PDF
```

Enter the page ranges:

```text
2-5, 8-10
```

The program will generate:

```text
output/
  pages_2-5.pdf
  pages_8-10.pdf
```

The GUI also supports dragging a PDF file directly into the Split PDF interface.

## Delete Pages

Select:

```text
3. Delete Pages
```

Enter the pages or page ranges to delete:

```text
2, 5-7, 10
```

The specified pages will be removed from the PDF.

For example, if the input PDF contains 10 pages and you enter:

```text
2, 5-7, 10
```

the program will keep pages:

```text
1, 3-4, 8-9
```

and generate:

```text
output/
  modified.pdf
```

The program validates the page ranges and prevents deleting all pages from the PDF.

If the output file already exists, the program will ask for confirmation before overwriting it.

## Testing

Run all tests with:

```bash
pytest
```

The project uses `pytest` and `pytest-qt` for automated testing.

The test suite covers:

- PDF merging
- PDF splitting
- Page deletion
- Page range validation
- File utilities
- CLI behavior
- GUI functionality
- Drag and drop functionality
- Multilingual GUI components
- User settings
- Database initialization
- SQLite schema
- Operation history repository
- Input validation

The current `v1.1.0` test suite passes:

```text
87 passed
```

## Code Quality

Run Ruff to check the code:

```bash
ruff check .
```

## Building the Windows Executable

The Windows executable is built using PyInstaller.

The project includes the PyInstaller specification file:

```text
PDF-Toolkit.spec
```

To build the application locally:

```bash
pyinstaller PDF-Toolkit.spec
```

The generated application will be placed in:

```text
dist/PDF-Toolkit/
```

The `build/` and `dist/` directories are excluded from Git.

## Continuous Integration

GitHub Actions automatically runs the project's test suite and code quality checks when changes are pushed to the repository.

The Windows build workflow also:

* Installs the required dependencies
* Runs the test suite
* Builds the Windows executable with PyInstaller
* Creates a distributable ZIP archive
* Uploads the Windows build as a GitHub Actions artifact

This ensures that the Windows executable is built from a tested version of the project.

## Current Version

**v1.1.0**

### v1.1.0 Highlights

* Added multilingual GUI support
* Added English, Chinese, and Japanese translations
* Added PDF drag-and-drop support
* Added drag-and-drop PDF reordering for merging
* Added Windows x64 executable build
* Added automated Windows executable packaging with GitHub Actions
* Expanded automated test coverage
* 87 tests currently passing

## License

This project is for learning and personal development.

## Author

Senyu Wu

GitHub: Senyu-Lab
