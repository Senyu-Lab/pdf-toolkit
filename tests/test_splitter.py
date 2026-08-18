from pathlib import Path

import pymupdf
import pytest

from app.splitter import (
    get_output_files,
    parse_page_ranges,
    split_pdf,
    validate_page_ranges,
)


def test_parse_single_range():
    result = parse_page_ranges("2-5")

    assert result == [(2, 5)]


def test_parse_multiple_ranges():
    result = parse_page_ranges("2-5,8-10")

    assert result == [(2, 5), (8, 10)]


def test_parse_ranges_with_spaces():
    result = parse_page_ranges("2-5, 8-10")

    assert result == [(2, 5), (8, 10)]

def test_invalid_range():
    with pytest.raises(ValueError):
        parse_page_ranges("8-2")

def test_invalid_page_number():
    with pytest.raises(ValueError):
        parse_page_ranges("abc-10")


def test_empty_range():
    with pytest.raises(ValueError):
        parse_page_ranges("2-5,,8-10")


def test_invalid_range_format():
    with pytest.raises(ValueError):
        parse_page_ranges("2-5-8")

def test_split_pdf(tmp_path: Path):
    input_file = tmp_path / "test.pdf"
    output_dir = tmp_path / "output"

    output_dir.mkdir()
    pdf = pymupdf.open()

    for _ in range(10):
        pdf.new_page()

    pdf.save(input_file)
    pdf.close()

    output_files = split_pdf(
        input_file,
        output_dir,
        [(2, 5)]
    )

    assert len(output_files) == 1
    assert output_files[0].exists()

    output_file = output_dir / "pages_2-5.pdf"
    assert output_file.exists()
    result_pdf = pymupdf.open(output_file)
    assert len(result_pdf) == 4

    result_pdf.close()

def test_split_pdf_multiple_ranges(tmp_path: Path):
    input_file = tmp_path / "test.pdf"
    output_dir = tmp_path / "output"

    output_dir.mkdir()
    pdf = pymupdf.open()

    for _ in range(10):
        pdf.new_page()

    pdf.save(input_file)
    pdf.close()

    output_files = split_pdf(
        input_file,
        output_dir,
        [(2, 5), (7, 10)]
    )

    assert len(output_files) == 2
    assert all(file.exists() for file in output_files)

    first_output = output_dir / "pages_2-5.pdf"
    second_output = output_dir / "pages_7-10.pdf"

    assert first_output.exists()
    assert second_output.exists()

    first_pdf = pymupdf.open(first_output)
    second_pdf = pymupdf.open(second_output)

    assert len(first_pdf) == 4
    assert len(second_pdf) == 4

    first_pdf.close()
    second_pdf.close()

def test_split_pdf_page_out_of_range(tmp_path: Path):
    input_file = tmp_path / "test.pdf"
    output_dir = tmp_path / "output"

    output_dir.mkdir()
    pdf = pymupdf.open()

    for _ in range(10):
        pdf.new_page()

    pdf.save(input_file)
    pdf.close()

    with pytest.raises(ValueError):
        split_pdf(
            input_file,
            output_dir,
            [(8, 12)]
        )

def test_get_output_files(tmp_path):
    result = get_output_files(
        tmp_path,
        [(2, 5), (8, 10)]
    )

    assert result == [
        tmp_path / "pages_2-5.pdf",
        tmp_path / "pages_8-10.pdf",
    ]

def test_validate_page_ranges():
    validate_page_ranges(
        [(2, 5), (8, 10)],
        10
    )



def test_validate_page_ranges_exceeds_page_count():
    with pytest.raises(ValueError):
        validate_page_ranges(
            [(8, 15)],
            10
        )

def test_validate_page_ranges_invalid_start():
    with pytest.raises(ValueError):
        validate_page_ranges(
            [(0, 5)],
            10
        )