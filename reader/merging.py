# two selected PDFs will be merged then a new PDF will be created of the newly merged PDFs
import PyPDF2


def merge_pdf(file, location):
    pdfMerger = PyPDF2.PdfFileMerger()

    for pdf in file:
        pdfMerger.append(pdf)

    with open(location, 'wb') as write:
        pdfMerger.write(write)
