# Import the required libraries
import tkinter
from tkinter import *
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

win = Tk()
win.geometry("700x250")


def open_win():
    root = tkinter.Toplevel()
    w1 = 800
    h = 650

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws / 2) - (w1 / 2)
    y = (hs / 2) - (h / 2)

    root.geometry('%dx%d+%d+%d' % (w1, h, x, y))
    root.title("PDF viewer")
    root.configure(bg="white")

    root_2 = tkinter.Toplevel()
    w1_2 = 800
    h_2 = 650

    ws_2 = root.winfo_screenwidth()
    hs_2 = root.winfo_screenheight()

    x_2 = (ws_2 / 2) - (w1_2 / 2)
    y_2 = (hs_2 / 2) - (h_2 / 2)

    root_2.geometry('%dx%d+%d+%d' % (w1_2, h_2, x_2, y_2))
    root_2.title("PDF viewer2")
    root_2.configure(bg="white")

    window = tkinter.Toplevel()
    window.geometry('150x50+300+215')
    window.title("Headings")

    merged = tkinter.Toplevel()
    merged.geometry('120x50+1500+215')
    merged.title("Merge")

    heading = []

    def browsefile():
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
        filename_two = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                  title="select pdf file",
                                                  filetypes=(("PDF File", ".pdf"),
                                                             ("PDF File", ".PDF"),
                                                             ("All file", ".txt")))

        return filename_two

    file = browsefile()

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

        return output

    # merging two different types of pdfs
    def two_merged():
        file_2 = browseFiles_two()
        pdfs = [file, file_2]
        output = 'pdfs_updated.pdf'
        PDFmerge(pdfs=pdfs, output=output)

        v1 = pdf.ShowPdf()
        v_2 = v1.pdf_view(root_2, pdf_location=open(output, "r"), width=77, height=100)
        v_2.pack(pady=(0, 0))

        root.destroy()
        root_2.mainloop()

    def clicked():
        top_window = tkinter.Toplevel(window)
        for ind, h in enumerate(heading):
            names_label = tkinter.Label(top_window)
            names_label.grid(row=int(ind) + 1, column=0)
            names_label.config(text=h)

        output = new_page()

        v1 = pdf.ShowPdf()
        v_2 = v1.pdf_view(root_2, pdf_location=open(output, "r"), width=77, height=100)
        v_2.pack(pady=(0, 0))

        root.destroy()
        root_2.mainloop()

    btn = Button(window, text="Print Headings", command=clicked)
    btn.grid(column=0, row=0, padx=30, pady=2)

    mg = tk.Button(merged, text='Merge', command=two_merged)
    mg.grid(column=0, row=0, padx=30, pady=2)

    win.iconify()
    root.mainloop()


Label(win, text=" ", font='Helvetica 18').place(relx=.5, rely=.5, anchor=CENTER)
Button(win, text="Open File", background="white", foreground="blue", font='Helvetica 13 bold', command=open_win).pack(
    pady=50)
win.mainloop()
