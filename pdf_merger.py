import pymupdf

def merge_pdfs(input_files, output_file):
    merged_pdf = pymupdf.open()

    for pdf_file in input_files:
        pdf = pymupdf.open(pdf_file)
        merged_pdf.insert_pdf(pdf)
        pdf.close()

    merged_pdf.save(output_file)
    merged_pdf.close()
