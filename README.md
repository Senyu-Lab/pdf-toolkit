# PDF Toolkit

A simple Python tool for merging and splitting PDF files.

## Features

- Merge multiple PDF files into one PDF
- Split a PDF by page ranges
- Support multiple page ranges
- Validate user input and page ranges
- Automated tests with pytest

## Requirements

- Python 3.10+
- PyMuPDF
- pypest

## Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Put PDF files into the input folder.\
Run
```bash
python main.py
```
Then choose an option from the menu.

## Current Version

v0.3.0

## Merge PDFs

Select:
```bash
1. Merge PDFs
```
The PDF files in the input directory will be merged into:
```bash
output/merged.pdf
```

## Split PDF

Select:
```bash
2. Split PDF
```
Enter the page ranges:
2-5,8-10\
The program will generate:
```bash
output/
  pages_2-5.pdf
  pages_8-10.pdf
```

## Testing

Run all tests with:
```bash
pytest
```

## License

This project is for learning and personal development.
