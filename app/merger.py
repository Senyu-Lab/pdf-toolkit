from pathlib import Path

import pymupdf

# Merge multiple PDF files into a single PDF.
def merge_pdfs(
    pdf_files: list[Path],
    output_file: Path
) -> None:

    output_pdf = pymupdf.open()

    # Add each PDF file to the output PDF.
    for pdf_file in pdf_files:
        pdf = pymupdf.open(pdf_file)
        output_pdf.insert_pdf(pdf)
        pdf.close()

    output_pdf.save(output_file)

    output_pdf.close()