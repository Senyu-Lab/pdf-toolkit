from pathlib import Path

from app.merger import merge_pdfs
from app.splitter import split_pdf,parse_page_ranges
from app.cli import get_page_number,get_page_ranges, show_menu
from app.file_utils import get_pdf_files,get_single_pdf



# Handle the PDF merge operation.
def handle_merge(input_dir: Path, output_dir: Path) -> None:
    pdf_files = get_pdf_files(input_dir)

    if not pdf_files:
        print("No PDF files found in the input folder.")
        return

    output_file = output_dir / "merged.pdf"
    merge_pdfs(pdf_files, output_file)

    print("PDF merge completed!")

# Handle the PDF split operation.
def handle_split(input_dir: Path, output_dir: Path) -> None:
    input_file = get_single_pdf(input_dir)

    if input_file is None:
        print("Please keep exactly one PDF in the input folder.")
        return

    page_ranges = get_page_ranges()

    try:
        split_pdf(
            input_file,
            output_dir,
            page_ranges
        )
        print("PDF split completed!")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    input_dir = Path("input")
    output_dir = Path("output")

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
            print("Invalid option.")


if __name__ == "__main__":
    main()