from pathlib import Path

import pymupdf
import pytest

from app.splitter import parse_page_ranges, split_pdf


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

    split_pdf(
        input_file,
        output_dir,
        [(2, 5)]
    )
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

    split_pdf(
        input_file,
        output_dir,
        [(2, 5), (7, 10)]
    )

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