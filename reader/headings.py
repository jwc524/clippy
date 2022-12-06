import fpdf
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser

heading_list = []


# methods for creating pdf files
def create_pdf(lists, location):
    # creates a new pdf page
    pdf_1 = fpdf.FPDF(format='letter')
    pdf_1.add_page()
    pdf_1.set_font("Times", size=15)

    # prints the list on a new pdf
    for i in lists:
        pdf_1.write(5, str(i))
        pdf_1.ln()
    pdf_1.output(location)


# parses through the pdf to find all the headings, appends it to list, then prints it on a new PDF
def find_headings(file):
    fp = open(file, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    # Get the outlines of the document.
    outlines = document.get_outlines()
    for (_, title, _, _, _) in outlines:
        heading_list.append(title)
    create_pdf(heading_list, location='heading.pdf')
    return heading_list
