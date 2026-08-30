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
* Persistent operation history with SQLite
* View operation details
* Delete selected history records
* Clear operation history
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
* Operation History

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

## Database and Operation History

PDF Toolkit uses SQLite for local persistence of PDF operation history.

The database layer is separated from the GUI and PDF processing logic. SQL statements are maintained separately from Python code to keep the database layer modular and maintainable.

The history system records PDF operations such as Merge and Split, including their status, input files, output files, and error information when applicable.

The History interface provides:

* View operation history
* Refresh history
* Delete selected records
* Clear all history
* View detailed operation information
* Track successful and failed operations

The database layer provides:

* SQLite database initialization
* Database connection management
* Operation history repository
* Insert operations
* Query operations
* Delete operations
* Clear operations
* Input validation
* Automated database tests

## Windows Executable

A pre-built Windows x64 executable is available from the GitHub Releases page.

### Download

Download the latest release:

```text
v1.2.0
```

The Windows release package will be provided as:

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

Successful and failed Merge operations are recorded in the operation history.

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
├── pages_2-5.pdf
└── pages_8-10.pdf
```

The GUI also supports dragging a PDF file directly into the Split PDF interface.

Successful and failed Split operations are recorded in the operation history.

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
└── modified.pdf
```

The program validates the page ranges and prevents deleting all pages from the PDF.

If the output file already exists, the program will ask for confirmation before overwriting it.

## Operation History

The History interface allows users to review previously completed PDF operations.

Each history record can include:

* Operation type
* Status
* Creation time
* Input files
* Output files
* Error information

### Delete Selected

Select a history record and choose **Delete Selected** to remove that record from the database.

### Clear History

Choose **Clear History** to remove all stored operation records after confirmation.

### Operation Details

Double-click a history record to open the operation details dialog.

The details dialog displays the complete information associated with the selected operation, including input files, output files, status, and error information when available.

## Testing

Run all tests with:

```bash
pytest
```

The project uses `pytest` and `pytest-qt` for automated testing.

The test suite covers:

* PDF merging
* PDF splitting
* Page deletion
* Page range validation
* File utilities
* CLI behavior
* GUI functionality
* Drag and drop functionality
* Multilingual GUI components
* User settings
* Database initialization
* SQLite schema
* Operation history repository
* HistoryWidget
* History details dialog
* Input validation

The current `v1.2.0` test suite passes:

```text
126 passed
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

v1.2.0

### v1.2.0 Highlights

* Added SQLite-based persistent operation history
* Added operation history management
* Added history refresh functionality
* Added selected history record deletion
* Added clear history functionality
* Added operation details dialog
* Added history records for Merge and Split operations
* Added success and failure status tracking
* Added error information to operation history
* Added automated tests for database and history functionality
* Expanded automated test coverage to 126 passing tests

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

## Author

Senyu Wu

GitHub: Senyu-Lab
