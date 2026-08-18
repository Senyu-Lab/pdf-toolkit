from pathlib import Path

from app.cli import get_confirmation, get_output_filename, get_page_ranges, show_menu
from app.file_utils import get_pdf_files, get_single_pdf
from app.merger import merge_pdfs
from app.splitter import (
    get_output_files,
    get_page_count,
    split_pdf,
    validate_page_ranges,
)


# Handle the PDF merge operation.
def handle_merge(input_dir: Path, output_dir: Path) -> None:
    pdf_files = get_pdf_files(input_dir)

    if not pdf_files:
        print("No PDF files found in the input folder.")
        return

    output_name = get_output_filename()

    output_file = output_dir / output_name
    # Ask for confirmation before overwriting an existing file.
    if output_file.exists():
        print()
        print("Output file already exists:")
        print(f"  {output_file}")

        if not get_confirmation("Overwrite?"):
            print("Merge cancelled.")
            return

    merge_pdfs(pdf_files, output_file)

    print("PDF merge completed!")
    print()
    print("Output file:")
    print(f"  {output_file.name}")

# Handle the PDF split operation.
def handle_split(input_dir: Path, output_dir: Path) -> None:
    input_file = get_single_pdf(input_dir)

    if input_file is None:
        print("Please keep exactly one PDF in the input folder.")
        return

    page_ranges = get_page_ranges()

    page_count = get_page_count(input_file)

    try:
        validate_page_ranges(
            page_ranges,
            page_count
        )
    except ValueError as e:
        print(f"Error: {e}")
        return

    output_files = get_output_files(
        output_dir,
        page_ranges
    )

    existing_files = [
        output_file
        for output_file in output_files
        if output_file.exists()
    ]

    # Ask for confirmation before overwriting existing files.
    if existing_files:
        print()
        print("Some output files already exist:")

        for output_file in existing_files:
            print(f"  {output_file.name}")

        if not get_confirmation("Overwrite existing files?"):
            print("Split cancelled.")
            return

    try:
        output_files = split_pdf(
            input_file,
            output_dir,
            page_ranges
        )

        print("PDF split completed!")
        print()
        print("Output files:")

        for output_file in output_files:
            print(f"  {output_file.name}")

    except ValueError as e:
        print(f"Error: {e}")


def main():
    input_dir = Path("input")
    output_dir = Path("output")

    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            handle_merge(input_dir, output_dir)

        elif choice == "2":
            handle_split(input_dir, output_dir)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-3.")


if __name__ == "__main__":
    main()