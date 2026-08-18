from pathlib import Path

import pymupdf

from app.merger import merge_pdfs


def test_merge_pdfs(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    output_file = tmp_path / "merged.pdf"

    first_pdf = input_dir / "first.pdf"
    second_pdf = input_dir / "second.pdf"

    pdf = pymupdf.open()
    pdf.new_page()
    pdf.new_page()
    pdf.save(first_pdf)
    pdf.close()

    pdf = pymupdf.open()
    pdf.new_page()
    pdf.new_page()
    pdf.new_page()
    pdf.save(second_pdf)
    pdf.close()

    merge_pdfs(
        [first_pdf, second_pdf],
        output_file
    )

    assert output_file.exists()

    merged_pdf = pymupdf.open(output_file)

    assert len(merged_pdf) == 5

    merged_pdf.close()

def test_merge_pdf_order(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    output_file = tmp_path / "merged.pdf"

    first_pdf = input_dir / "first.pdf"
    second_pdf = input_dir / "second.pdf"

    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((100, 100), "FIRST")
    pdf.save(first_pdf)
    pdf.close()

    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((100, 100), "SECOND")
    pdf.save(second_pdf)
    pdf.close()

    merge_pdfs(
        [first_pdf, second_pdf],
        output_file
    )

    merged_pdf = pymupdf.open(output_file)

    first_text = merged_pdf[0].get_text()
    second_text = merged_pdf[1].get_text()

    assert "FIRST" in first_text
    assert "SECOND" in second_text

    merged_pdf.close()
