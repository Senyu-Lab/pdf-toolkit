from app.file_utils import is_valid_output_filename
from app.splitter import parse_page_ranges


# Display the main menu.
def show_menu() -> None:
    print()
    print("=" * 32)
    print("          PDF Toolkit")
    print("=" * 32)
    print()
    print("1. Merge PDFs")
    print("2. Split PDF")
    print("3. Delete Pages")
    print("4. Exit")
    print()

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
        page_range = input("Enter page ranges (e.g. 2-5, 8-10): ")

        try:
            return parse_page_ranges(page_range)
        except ValueError as e:
            print(f"Error: {e}")

# Ask the user for a yes or no confirmation.
def get_confirmation(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()

        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please enter y or n.")

# Get a valid output filename from the user.
def get_output_filename(default: str = "merged.pdf") -> str:
    while True:
        filename = input(
            f"Output filename (default: {default}): "
        ).strip()

        if not filename:
            filename = default

        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        if is_valid_output_filename(filename):
            return filename

        print("Invalid filename. Please enter a filename only.")