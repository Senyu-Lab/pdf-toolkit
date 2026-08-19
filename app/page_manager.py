from pathlib import Path

import pymupdf


# Delete the specified pages and save the remaining pages to a new PDF.
def delete_pages(
    input_file: Path,
    output_file: Path,
    page_ranges: list[tuple[int, int]],
) -> None:
    doc = pymupdf.open(input_file)

    page_count = len(doc)

    pages_to_delete = set()

    for start, end in page_ranges:
        if start < 1 or end > page_count or start > end:
            doc.close()
            raise ValueError("Page range is out of bounds.")

        for page_number in range(start, end + 1):
            pages_to_delete.add(page_number - 1)

    if len(pages_to_delete) >= page_count:
        doc.close()
        raise ValueError("Cannot delete all pages.")

    for page_number in sorted(pages_to_delete, reverse=True):
        doc.delete_page(page_number)

    doc.save(output_file)
    doc.close()