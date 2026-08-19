from pathlib import Path

import pymupdf
import pytest

from app.page_manager import delete_pages


def create_test_pdf(file_path: Path, page_count: int) -> None:
    doc = pymupdf.open()

    for _ in range(page_count):
        doc.new_page()

    doc.save(file_path)
    doc.close()


def get_page_count(file_path: Path) -> int:
    doc = pymupdf.open(file_path)
    page_count = len(doc)
    doc.close()

    return page_count


def test_delete_single_page(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 5)

    delete_pages(
        input_file,
        output_file,
        [(3, 3)],
    )

    assert get_page_count(output_file) == 4


def test_delete_page_range(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 10)

    delete_pages(
        input_file,
        output_file,
        [(3, 5)],
    )

    assert get_page_count(output_file) == 7


def test_delete_multiple_ranges(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 10)

    delete_pages(
        input_file,
        output_file,
        [(2, 2), (5, 7), (10, 10)],
    )

    assert get_page_count(output_file) == 5


def test_cannot_delete_all_pages(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 5)

    with pytest.raises(ValueError):
        delete_pages(
            input_file,
            output_file,
            [(1, 5)],
        )


def test_page_range_out_of_bounds(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"

    create_test_pdf(input_file, 5)

    with pytest.raises(ValueError):
        delete_pages(
            input_file,
            output_file,
            [(6, 6)],
        )