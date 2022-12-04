# change PyMuPDF to version 1.18.17
import os
from tkinter import *
from tkinter import filedialog
import tkinter
import PyPDF2
import fpdf
from tkPDFViewer import tkPDFViewer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

width, height = 800, 650


# aligns the GUI to the center of the screen
def align_center(window, w, h):
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


# creating the main window of the application
main_window = Tk()
align_center(main_window, 700, 250)
main_window.title("PDF Viewer")


# the start of the application
def open_files():
    # all windows created and aligned
    pdf_window = tkinter.Toplevel()
    align_center(pdf_window, 800, 650)

    updated_pdf = tkinter.Toplevel()
    align_center(updated_pdf, 800, 650)

    headings = tkinter.Toplevel()
    headings.geometry('150x50+300+215')
    headings.title("Headings")

    merge = tkinter.Toplevel()
    merge.geometry('120x50+1500+215')
    merge.title("Merge")

    rotate = tkinter.Toplevel()
    rotate.geometry('120x50+1500+810')
    rotate.title("rotate")

    resize_window = tkinter.Toplevel()
    resize_window.geometry('150x100+300+765')
    resize_window.title('Resizing')

    heading_list = []

    # lets the user resize the given window
    def resize(c):
        global width, height
        if c == 'increase':
            width = width + 20
            height = height + 20
        elif c == 'decrease':
            width = width - 20
            height = height - 20

        d = str(width) + 'x' + str(height)
        pdf_window.geometry(d)

    # allows users to select the file that they want to read: PDFs and TXT files
    def file_dir():
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="select pdf file",
                                              filetypes=(("PDF File", ".pdf"),
                                                         ("PDF File", ".PDF"),
                                                         ("All file", ".txt")))
        return filename

    # creates the window in which the PDF will be loaded onto
    def upload_file(filename, window, w, h):
        v1 = tkPDFViewer.ShowPdf()
        v2 = v1.pdf_view(window, pdf_location=open(filename, "r"), width=w, height=h)
        v2.pack(pady=(0, 0))

    main_file = file_dir()
    upload_file(main_file, pdf_window, 77, 100)

    # parses through the pdf to find all the headings, appends it to list, then prints it on a new PDF
    def find_headings():
        fp = open(main_file, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        # Get the outlines of the document.
        outlines = document.get_outlines()
        for (_, title, _, _, _) in outlines:
            heading_list.append(title)

        # creates a page where headings are located
        pdf_1 = fpdf.FPDF(format='letter')
        pdf_1.add_page()
        pdf_1.set_font("Arial", size=15)

        # prints the heading on a new pdf
        for i in heading_list:
            pdf_1.write(5, str(i))
            pdf_1.ln()
        pdf_1.output("heading.pdf")

    # two selected PDFs will be merged then a new PDF will be created of the newly merged PDFs
    def merge_pdf(file, location):
        pdfMerger = PyPDF2.PdfFileMerger()

        for pdf in file:
            pdfMerger.append(pdf)

        with open(location, 'wb') as write:
            pdfMerger.write(write)

    # merges the heading and selected file together so that users can have a list of all the headings before reading
    def pdf_heading(file):
        pdfs = ['heading.pdf', file]
        location = 'print_heading.pdf'
        merge_pdf(file=pdfs, location=location)

        return location

    # merges two selected PDFs together
    def multiple_pdf():
        second_file = file_dir()
        pdfs = [main_file, second_file]
        location = 'pdf_merge.pdf'

        merge_pdf(file=pdfs, location=location)

        upload_file(location, updated_pdf, 77, 100)

        # updating the tkinter window
        pdf_window.destroy()
        updated_pdf.mainloop()

    # creating a small window where headings are upload for a greater user experience
    def print_heading():
        find_headings()
        top_window = tkinter.Toplevel(headings)
        for ind, h in enumerate(heading_list):
            names_label = tkinter.Label(top_window)
            names_label.grid(row=int(ind) + 1, column=0)
            names_label.config(text=h)

        output = pdf_heading(main_file)
        upload_file(output, updated_pdf, 77, 100)

        # updating the tkinter window
        pdf_window.destroy()
        updated_pdf.mainloop()

    # rotates selected PDF 90 degrees every click
    def rotate_pdf(file, location, rotation):
        pdf_file = open(file, 'rb')

        pdf_reader = PyPDF2.PdfFileReader(main_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page in range(pdf_reader.numPages):
            pageObj = pdf_writer.getPage(page)
            pageObj.rotateClockwise(rotation)

            pdf_writer.addPage(pageObj)

        updated_file = open(location, 'wb')
        pdf_writer.write(updated_file)

        pdf_file.close()
        updated_file.close()

    # creates a tkinter window for the rotated PDF
    def upload_rotation():
        file = main_file
        location = 'rotate.pdf'
        rotate_pdf(file=file, location=location, rotation=90)

        upload_file(location, updated_pdf, 100, 100)

        pdf_window.destroy()
        updated_pdf.mainloop()

    # giving the user full control in what they want to do with selected PDFs
    head_button = Button(headings, text="Print Headings", command=print_heading)
    head_button.grid(column=0, row=0, padx=33, pady=10)

    merge_button = tkinter.Button(merge, text='Merge', command=multiple_pdf)
    merge_button.grid(column=0, row=0, padx=40, pady=10)

    rotate_button = tkinter.Button(rotate, text='Rotate', command=upload_rotation)
    rotate_button.grid(column=0, row=0, padx=40, pady=10)

    increase_zoom = tkinter.Button(resize_window, text='zoom++', command=lambda: resize('increase'))
    increase_zoom.grid(column=0, row=0, padx=50, pady=10)

    decrease_zoom = tkinter.Button(resize_window, text='zoom++', command=lambda: resize('decrease'))
    decrease_zoom.grid(column=0, row=1, padx=50, pady=10)

    # destroying the main window will close our application, instead we minimize it
    main_window.iconify()
    pdf_window.mainloop()


Label(main_window, text=" ", font='Helvetica 18').place(relx=.5, rely=.5, anchor=CENTER)
Button(main_window, text="Open File", background="white", foreground="red", font='Helvetica 13 bold',
       command=open_files).pack(
    pady=50)

# executing the window
main_window.mainloop()
