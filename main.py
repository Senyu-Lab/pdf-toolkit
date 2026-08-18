from pathlib import Path

from pdf_merger import merge_pdfs
from pdf_splitter import split_pdf,parse_page_ranges


def get_pdf_files(input_dir):
    return sorted(input_dir.glob("*.pdf"))


def show_menu():
    print("================================")
    print("          PDF Toolkit")
    print("================================")
    print()
    print("1. Merge PDF")
    print("2. Split PDF")
    print("3. Exit")

# Get an integer from user input.
def get_page_number(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# Get page ranges from user input.
def get_page_ranges() -> list[tuple[int, int]]:
    while True:
        page_range = input("Page ranges: ")
        try:
            return parse_page_ranges(page_range)
        except ValueError as e:
            print(f"Error: {e}")

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

def main():
    input_dir = Path("input")
    output_dir = Path("output")

    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            pdf_files = get_pdf_files(input_dir)

            if not pdf_files:
                print("No PDF files found in the input folder.")
            else:
                output_file = output_dir / "merged.pdf"
                merge_pdfs(pdf_files, output_file)
                print("PDF merge completed!")




        elif choice == "2":
            pdf_file = get_single_pdf(input_dir)

            if pdf_file is not None:
                page_ranges = get_page_ranges()

                try:
                    split_pdf(
                        pdf_file,
                        output_dir,
                        page_ranges
                    )
                    print("PDF split completed!")

                except ValueError as e:
                    print(f"Error: {e}")


        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()