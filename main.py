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