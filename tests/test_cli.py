import pymupdf

from app.cli import get_confirmation, get_output_filename
from main import handle_delete_pages


def test_get_confirmation_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")

    assert get_confirmation("Overwrite?") is True


def test_get_confirmation_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")

    assert get_confirmation("Overwrite?") is False

def test_get_confirmation_invalid_input(monkeypatch):
    answers = iter(["abc", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert get_confirmation("Overwrite?") is True


def test_get_output_filename(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "report")

    assert get_output_filename() == "report.pdf"

def test_get_output_filename_invalid_then_valid(monkeypatch):
    answers = iter(["../report", "report"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert get_output_filename() == "report.pdf"

def test_get_output_filename_default(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    assert get_output_filename() == "merged.pdf"

def test_handle_delete_pages(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    input_file = input_dir / "input.pdf"

    doc = pymupdf.open()
    for _ in range(5):
        doc.new_page()
    doc.save(input_file)
    doc.close()

    monkeypatch.setattr(
        "main.get_page_ranges",
        lambda: [(3, 3)],
    )

    handle_delete_pages(input_dir, output_dir)

    output_file = output_dir / "modified.pdf"

    assert output_file.exists()

    doc = pymupdf.open(output_file)
    assert len(doc) == 4
    doc.close()


def test_handle_delete_pages_cancel_overwrite(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    input_file = input_dir / "input.pdf"
    output_file = output_dir / "modified.pdf"

    doc = pymupdf.open()
    for _ in range(5):
        doc.new_page()
    doc.save(input_file)
    doc.close()

    output_file.write_bytes(b"existing file")

    monkeypatch.setattr(
        "main.get_page_ranges",
        lambda: [(3, 3)],
    )

    monkeypatch.setattr(
        "main.get_confirmation",
        lambda prompt: False,
    )

    handle_delete_pages(input_dir, output_dir)

    assert output_file.read_bytes() == b"existing file"