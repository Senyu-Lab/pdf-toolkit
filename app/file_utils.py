from pathlib import Path


def get_pdf_files(input_dir):
    return sorted(input_dir.glob("*.pdf"))

# Get the only PDF file from the input directory.
def get_single_pdf(input_dir: Path) -> Path | None:
    pdf_files = get_pdf_files(input_dir)

    if not pdf_files:
        print("No PDF files found in the input folder.")
        return None

    if len(pdf_files) > 1:
        print("Please keep only one PDF in the input folder.")
        return None

    return pdf_files[0]

# Check whether the filename is safe to use as an output filename.
def is_valid_output_filename(filename: str) -> bool:
    path = Path(filename)

    return (
        filename != ""
        and path.name == filename
    )