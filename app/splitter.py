from pathlib import Path

import pymupdf

# Parse and validate page ranges entered by the user.
def parse_page_ranges(page_range: str) -> list[tuple[int, int]]:
    ranges = page_range.split(",")

    result = []

    for page_range_item in ranges:
        page_range_item = page_range_item.strip()

        if not page_range_item:
            raise ValueError("Page range cannot be empty.")

        parts = page_range_item.split("-")

        if len(parts) != 2:
            raise ValueError(f"Invalid page range: {page_range_item}")

        try:
            start = int(parts[0])
            end = int(parts[1])

        except ValueError:
            raise ValueError(f"Invalid page range: {page_range_item}")

        if start < 1 or end < 1:
            raise ValueError( "Page numbers must be at least 1.")

        if start > end:
            raise ValueError(f"Invalid page range: {page_range_item}")

        result.append((start, end))

    return result

# Split a PDF into multiple files based on page ranges.
def split_pdf(
    input_file: Path,
    output_dir: Path,
    page_ranges: list[tuple[int, int]]
) -> None:

    pdf = pymupdf.open(input_file)

    page_count = len(pdf)

    for start_page, end_page in page_ranges:
        if end_page > page_count:
            raise ValueError(f"End page must be no more than {page_count}.")

        output_pdf = pymupdf.open()

        # Convert user page numbers to zero-based indexes used by PyMuPDF.
        start_index = start_page - 1
        end_index = end_page - 1

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

