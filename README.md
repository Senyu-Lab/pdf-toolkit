# PDF Toolkit

[![CI](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml)

A simple Python tool for merging, splitting, and editing PDF files.

## Features

* Merge multiple PDF files into one PDF
* Split a PDF by page ranges
* Delete specific pages or page ranges from a PDF
* Support multiple page ranges
* Validate user input and page ranges
* Command-line interface (CLI)
* Graphical user interface (GUI) built with PySide6

## Requirements

* Python 3.10+
* PyMuPDF
* PySide6
* pytest
* Ruff

## Installation

Clone the repository and install the dependencies:

```bash
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

## Current Version

v1.0.0

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

The project includes automated tests covering PDF merging, splitting, page deletion, input validation, CLI behavior, and GUI functionality.

## Code Quality

Run Ruff to check the code:

```bash
ruff check .
```

## Continuous Integration

GitHub Actions automatically runs the test suite and code quality checks when changes are pushed to the repository.

## License

This project is for learning and personal development.
