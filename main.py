from pathlib import Path

from pdf_merger import merge_pdfs
from pdf_splitter import split_pdf


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
            pdf_files = get_pdf_files(input_dir)

            if not pdf_files:
                print("No PDF files found in the input folder.")
            elif len(pdf_files) > 1:
                print("Please keep only one PDF in the input folder.")
            else:
                split_pdf(pdf_files[0], output_dir)
                print("PDF split completed!")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()