import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import PyPDF2
import fpdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from tkPDFViewer import tkPDFViewer as pdf  # change version to 1.18.17
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# creating up popup windows
root = Tk()
root.geometry("630x700+400+100")
root.title("PDF viewer")
root.configure(bg="white")

window = tk.Tk()
window.title("Headings")

w = tk.Tk()
w.title("Merge")

heading = []


#  browsing files through local directories to open files
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


def browseFiles_two():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="select pdf file",
                                          filetypes=(("PDF File", ".pdf"),
                                                     ("PDF File", ".PDF"),
                                                     ("All file", ".txt")))
    return filename


# stores the file selected into a variable
file = browseFiles()

# obtaining the table of contents to the file selected
fp = open(file, 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)

# Get the outlines of the document.
outlines = document.get_outlines()
for (_, title, _, _, _) in outlines:
    heading.append(title)

# creates a page where headings are located
pdf_1 = fpdf.FPDF(format='letter')
pdf_1.add_page()
pdf_1.set_font("Arial", size=15)

# prints the heading on a new pdf
for i in heading:
    pdf_1.write(5, str(i))
    pdf_1.ln()
pdf_1.output("heading.pdf")


# merging two pdfs together
def PDFmerge(pdfs, output):
    pdfMerger = PyPDF2.PdfFileMerger()

    for pdf in pdfs:
        pdfMerger.append(pdf)

    with open(output, 'wb') as f:
        pdfMerger.write(f)


# when user clicks for the heading, a new pdf is created
def new_page():
    pdfs = ['heading.pdf', file]

    # output pdf file name
    output = 'merged.pdf'

    # calling pdf merge function
    PDFmerge(pdfs=pdfs, output=output)


# merging two different types of pdfs
def two_merged():
    file_2 = browseFiles_two()
    pdfs = [file, file_2]
    output = 'pdfs_updated.pdf'
    PDFmerge(pdfs=pdfs, output=output)
    subprocess.Popen(['pdfs_updated.pdf'], shell=True)


# what happens when heading is clicked
def clicked():
    top_window = tk.Toplevel(window)
    for ind, h in enumerate(heading):
        names_label = tk.Label(top_window)
        names_label.grid(row=int(ind) + 1, column=0)
        names_label.config(text=h)
    subprocess.Popen(['links.pdf'], shell=True)


# how users are able to click on certain parts of the selected pdf
def links():
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open('merged.pdf', 'rb'))

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

    # Figure One
    pdf_writer.addLink(pagenum=1, pagedest=2, rect=RectangleObject([407, 194, 417, 205]), )

    with open(os.path.abspath('links.pdf'), 'wb') as link_pdf:
        pdf_writer.write(link_pdf)


# creating the buttons
btn = tk.Button(window, text="Print Headings", command=clicked)
btn.grid(column=0, row=0, padx=30, pady=2)

mg = tk.Button(w, text='Merge', command=two_merged)
mg.grid(column=0, row=0, padx=30, pady=2)


def main():
    new_page()
    links()

    root.mainloop()


if __name__ == '__main__':
    main()
