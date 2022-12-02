# import camelot.io as camelot
# # from tabula.io import read_pdf
#
# # extract all the tables in the PDF file
# abc = camelot.read_pdf("BURT.pdf")  # address of file location
#
# # print the first table as Pandas DataFrame
# print(abc[0].df)
#
# # from pdfreader import PDFDocument, SimplePDFViewer
# #
# # file_name = "BURT.pdf"
# #
# # fd = open(file_name, "rb")
# # viewer = SimplePDFViewer(fd)
# #
# # for canvas in viewer:
# #     page_img = canvas.images
# #     page_forms = canvas.forms
# #     page_txt = canvas.text_content
# #     page_inline_img = canvas.inline_images
# #     page_strings = canvas.strings
# #
# # viewer.navigate(1)
# # viewer.render()
# # print(viewer.canvas.strings)
# # print(viewer.canvas.text_content)
# #
# # import pdfplumber
# #
# # file_name = 'BURT.pdf'
# #
# # with pdfplumber.open(file_name) as pdf:
# #     page = pdf.pages[12]
# #     print(page.extract_text())
#
#
#
#
# # # STEP 1
# # # import libraries
# # import fitz
# # import io
# # from PIL import Image
# #
# # # STEP 2
# # # file path you want to extract images from
# # file = "BURT.pdf"
# #
# # # open the file
# # pdf_file = fitz.open(file)
# #
# # # STEP 3
# # # iterate over PDF pages
# # for page_index in range(len(pdf_file)):
# #
# #     # get the page itself
# #     page = pdf_file[page_index]
# #     image_list = page.getImageList()
# #
# #     # printing number of images found in this page
# #     if image_list:
# #         print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
# #     else:
# #         print("[!] No images found on page", page_index)
# #     for image_index, img in enumerate(page.getImageList(), start=1):
# #         # get the XREF of the image
# #         xref = img[0]
# #
# #         # extract the image bytes
# #         base_image = pdf_file.extractImage(xref)
# #         image_bytes = base_image["image"]
# #
# #         # get the image extension
# #         image_ext = base_image["ext"]
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
    output = 'merged.pdf'

    # calling pdf merge function
    PDFmerge(pdfs=pdfs, output=output)


def clicked():
    top_window = tk.Toplevel(window)
    for ind, h in enumerate(heading):
        names_label = tk.Label(top_window)
        names_label.grid(row=int(ind) + 1, column=0)
        names_label.config(text=h)
    subprocess.Popen(['links.pdf'], shell=True)


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


btn = tk.Button(window, text="Print Headings", command=clicked)
btn.grid(column=0, row=0, padx=30, pady=2)


def main():
    new_page()
    links()

    root.mainloop()


if __name__ == '__main__':
    main()
