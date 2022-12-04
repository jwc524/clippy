from pdfminer.high_level import *
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


def get_headings(path):
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    headings = {}

    # Get the outlines of the document.
    outlines = document.get_outlines()
    for (_, title, _, a, _) in outlines:
        headings.update({title: a})

    return headings
