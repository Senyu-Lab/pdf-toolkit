# PDF Toolkit
[![CI](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml)

A simple Python command-line tool for merging and splitting PDF files.

## Features

* Merge multiple PDF files into one PDF
* Split a PDF by page ranges
* Support multiple page ranges
* Validate user input and page ranges
* Validate output filenames
* Handle existing output files safely
* Automated tests with pytest
* Code quality checks with Ruff
* Continuous Integration with GitHub Actions

## Requirements

* Python 3.10+
* PyMuPDF
* pytest
* Ruff

## Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place PDF files into the `input` folder.

Run the program:

```bash
python main.py
```

Then choose an option from the menu.

### Merge PDFs

Select:

```text
1. Merge PDFs
```

All PDF files in the `input` directory will be merged into:

```text
output/merged.pdf
```

### Split PDF

Select:

```text
2. Split PDF
```

Enter one or more page ranges.

For example:

```text
2-5,8-10
```

The program will generate separate PDF files:

```text
output/
├── pages_2-5.pdf
└── pages_8-10.pdf
```

Multiple page ranges are supported.



## Testing

Run all tests with:

```bash
pytest
```

The project currently includes automated tests for the CLI, file utilities, PDF merging, and PDF splitting.

## Code Quality

Ruff is used for code quality and import checking.

Run Ruff with:

```bash
ruff check .
```

Ruff can automatically fix supported issues with:

```bash
ruff check . --fix
```

## Continuous Integration

GitHub Actions automatically runs the test suite and Ruff checks when changes are pushed to the `main` branch or when a pull request is opened.

The CI workflow verifies that:

* All tests pass
* Ruff checks pass

## Current Version

v0.4.0

## License

This project is for learning and personal development.
