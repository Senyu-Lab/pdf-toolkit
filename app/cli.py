from app.splitter import parse_page_ranges

# Display the main menu.
def show_menu():
    print("\n=== PDF Toolkit ===")
    print("1. Merge PDFs")
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

