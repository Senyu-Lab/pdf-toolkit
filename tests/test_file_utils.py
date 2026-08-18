from app.file_utils import is_valid_output_filename


def test_valid_output_filename():
    assert is_valid_output_filename("report.pdf") is True
    assert is_valid_output_filename("my report.pdf") is True
    assert is_valid_output_filename("报告.pdf") is True


def test_invalid_output_filename():
    assert is_valid_output_filename("../report.pdf") is False
    assert is_valid_output_filename("folder/report.pdf") is False
    assert is_valid_output_filename("folder\\report.pdf") is False