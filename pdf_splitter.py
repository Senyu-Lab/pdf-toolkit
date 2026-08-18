from pathlib import Path

import pymupdf

# Split a PDF by a specified page range.
def split_pdf(
    input_file: Path,
    output_dir: Path,
    start_page: int,
    end_page: int
) -> None:

    pdf = pymupdf.open(input_file)

    page_count = len(pdf)

    # Check
    if start_page < 1:
        raise ValueError("Start page must be at least 1.")
    if end_page > page_count:
        raise ValueError(f"End page must be no more than {page_count}.")
    if start_page > end_page:
        raise ValueError("Start page must not be greater than end page.")

    output_pdf = pymupdf.open()

    # Convert user page numbers to Python indexes.
    start_index = start_page - 1
    end_index = end_page - 1

    # Copy the selected pages to the new PDF.
    for page_number in range(start_index, end_index + 1):
        output_pdf.insert_pdf(
            pdf,
            from_page=page_number,
            to_page=page_number
        )

    output_file = output_dir / f"pages_{start_page}-{end_page}.pdf"

    output_pdf.save(output_file)

    output_pdf.close()
    pdf.close()

