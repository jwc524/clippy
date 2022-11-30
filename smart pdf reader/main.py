import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
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
for (level, title, dest, a, se) in outlines:
    heading.append(title)


def clicked():
    top_window = tk.Toplevel(window)
    for ind, fruit in enumerate(heading):
        names_label = tk.Label(top_window)
        names_label.grid(row=int(ind) + 1, column=0)
        names_label.config(text=fruit)


btn = tk.Button(window, text="Print Headings", command=clicked)
btn.grid(column=0, row=0, padx=30, pady=2)

Button(root, text="open", command=browseFiles, width=40,
       font="arial 20", bd=4).pack()

root.mainloop()

# Open a PDF document.
