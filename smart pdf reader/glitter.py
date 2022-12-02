import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk

import PyPDF2
import fpdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from tkPDFViewer import tkPDFViewer as pdf  # change version to 1.18.17
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

root = Tk()
root.geometry("630x700+400+100")
root.title("PDF viewer")
root.configure(bg="white")

window = tk.Tk()
window.title("Headings")

heading = []


def browseFiles():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="select pdf file",
                                          filetypes=(("PDF File", ".pdf"),
                                                     ("PDF File", ".PDF"),
                                                     ("All file", ".txt")))

    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(root, pdf_location=open(filename, "r"), width=77, height=100)
    v2.pack(pady=(0, 0))

    return filename


file = browseFiles()

fp = open(file, 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)

# Get the outlines of the document.
outlines = document.get_outlines()
for (_, title, _, _, _) in outlines:
    heading.append(title)

# creates a page where headings are location
pdf = fpdf.FPDF(format='letter')
pdf.add_page()
pdf.set_font("Arial", size=15)

for i in heading:
    pdf.write(5, str(i))
    pdf.ln()
pdf.output("heading.pdf")


# need to merge the two pdfs together
def PDFmerge(pdfs, output):
    # creating pdf file merger object
    pdfMerger = PyPDF2.PdfFileMerger()

    # appending pdfs one by one
    for pdf in pdfs:
        pdfMerger.append(pdf)

    # writing combined pdf to output pdf file
    with open(output, 'wb') as f:
        pdfMerger.write(f)


def new_page():
    pdfs = ['heading.pdf', file]

    # output pdf file name
    output = 'new_file.pdf'

    # calling pdf merge function
    PDFmerge(pdfs=pdfs, output=output)


def clicked():
    top_window = tk.Toplevel(window)
    for ind, h in enumerate(heading):
        names_label = tk.Label(top_window)
        names_label.grid(row=int(ind) + 1, column=0)
        names_label.config(text=h)


btn = tk.Button(window, text="Print Headings", command=clicked)
btn.grid(column=0, row=0, padx=30, pady=2)

new_page()

pdf_writer = PdfFileWriter()
pdf_reader = PdfFileReader(open('new_file.pdf', 'rb'))

num_of_pages = pdf_reader.getNumPages()

for page in range(num_of_pages):
    current_page = pdf_reader.getPage(page)
    pdf_writer.addPage(current_page)

# dimensions is 612x792
# Abstract to Question for Detection
pdf_writer.addLink(pagenum=0, pagedest=1, rect=RectangleObject([20, 715, 200, 765]), )

# Search for Answer to Nodejs Glitter Data
pdf_writer.addLink(pagenum=0, pagedest=2, rect=RectangleObject([20, 655, 200, 713]), )

# Classifier to Results
pdf_writer.addLink(pagenum=0, pagedest=3, rect=RectangleObject([20, 615, 200, 653]), )

# Related Works to Conclusion and Future Work
pdf_writer.addLink(pagenum=0, pagedest=4, rect=RectangleObject([20, 540, 200, 613]), )

# References
pdf_writer.addLink(pagenum=0, pagedest=5, rect=RectangleObject([20, 520, 200, 538]), )

with open(os.path.abspath('new_file_1.pdf'), 'wb') as link_pdf:
    pdf_writer.write(link_pdf)

root.mainloop()
