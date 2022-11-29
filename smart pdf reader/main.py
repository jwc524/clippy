# to open document with GUI
import os
from tkinter import *
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf # change version to 1.18.17

root = Tk()
root.geometry("630x700+400+100")
root.title("PDF viewer")
root.configure(bg="white")


def browseFiles():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="select pdf file",
                                          filetypes=(("PDF File", ".pdf"),
                                                     ("PDF File", ".PDF"),
                                                     ("All file", ".txt")))

    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(root, pdf_location=open(filename, "r"), width=77, height=100)
    v2.pack(pady=(0, 0))


Button(root, text="open", command=browseFiles, width=40,
       font="arial 20", bd=4).pack()
root.mainloop()



# To open document and print all the headings
import password as password
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# Open a PDF document.
fp = open('BURT.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser, password)

# Get the outlines of the document.
outlines = document.get_outlines()
for (level, title, dest, a, se) in outlines:
    print(level, title)


  #ORIGINAL
# import pdfreader
# from pdfreader import PDFDocument, SimplePDFViewer

# file_name = "example.pdf"

# fd =  open(file_name, "rb")
# viewer = SimplePDFViewer(fd)

# for canvas in viewer:
#     page_img = canvas.images
#     page_forms = canvas.forms
#     page_txt = canvas.text_content
#     page_inline_img = canvas.inline_images
#     page_strings = canvas.strings

# viewer.navigate(1)
# viewer.render()
# print(viewer.canvas.strings)
# ##viewer.canvas.text_content
