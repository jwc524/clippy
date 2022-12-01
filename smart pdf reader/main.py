import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk

import PyPDF2
import fpdf
from tkPDFViewer import tkPDFViewer as pdf  # change version to 1.18.17
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from summarizer import summarize

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

print(summarize(filename))

new_page()
root.mainloop()
