from app.cli import get_confirmation, get_output_filename


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

