import pymupdf


def split_pdf(input_file, output_dir):
    pdf = pymupdf.open(input_file)

    page_count = len(pdf)

    for page_number in range(page_count):
        output_pdf = pymupdf.open()

        output_pdf.insert_pdf(
            pdf,
            from_page=page_number,
            to_page=page_number
        )

        output_file = output_dir / f"page_{page_number + 1}.pdf"

        output_pdf.save(output_file)
        output_pdf.close()

    pdf.close()
