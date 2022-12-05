# change PyMuPDF to version 1.18.17
import os
import PyPDF2
import fpdf

import tkinter
from tkinter import *
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from summarizer_beta import get_summary
from summarizer_beta import get_extracted_text
from summarizer_beta import common_words_graph

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
    # all pdf windows created and aligned
    pdf_window = tkinter.Toplevel()
    align_center(pdf_window, 800, 650)

    updated_pdf = tkinter.Toplevel()
    align_center(updated_pdf, 800, 650)

    # all button windows created and aligned
    buttons = tkinter.Toplevel()
    buttons.geometry('250x350+300+215')
    buttons.title("Headings")

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
        # pdf_window.geometry(d)
        updated_pdf.geometry(d)

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

    # method for creating pop-up windows
    def pop_windows(p_window, lists):
        for ind, h in enumerate(lists):
            names_label = tkinter.Label(p_window)
            names_label.grid(row=int(ind) + 1, column=0)
            names_label.config(text=h)

    # parses through the pdf to find all the headings, appends it to list, then prints it on a new PDF
    def find_headings(file):
        fp = open(file, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        # Get the outlines of the document.
        outlines = document.get_outlines()
        for (_, title, _, _, _) in outlines:
            heading_list.append(title)

        create_pdf(heading_list, 'heading.pdf')

    # two selected PDFs will be merged then a new PDF will be created of the newly merged PDFs
    def merge_pdf(file, location):
        pdfMerger = PyPDF2.PdfFileMerger()

        for pdf in file:
            pdfMerger.append(pdf)

        with open(location, 'wb') as write:
            pdfMerger.write(write)

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
        find_headings(main_file)

        top_window = tkinter.Toplevel(buttons)
        top_window.geometry('+225+335')
        pop_windows(top_window, heading_list)

    # rotates selected PDF 90 degrees every click
    def rotate_pdf(file, location, rotation):
        pdf_file = open(file, 'rb')

        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page in range(pdf_reader.numPages):
            page_num = pdf_reader.getPage(page)
            page_num.rotateClockwise(rotation)

            pdf_writer.addPage(page_num)

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

    # gets the summary of the select PDF
    def print_summary():
        path = main_file
        summary_contents = get_summary(path)

        genre = summary_contents[0][0]
        score = summary_contents[0][1]
        p_summary = summary_contents[1]

        data = [genre, score, p_summary]

        s_window = tkinter.Toplevel(buttons)
        s_window.geometry('+900+100')
        pop_windows(s_window, data)

        text = get_extracted_text(path)
        common_words_graph(text)

    # giving the user full control in what they want to do with selected PDFs
    Button(buttons, text="Print Headings", command=print_heading).grid(padx=33, pady=10)
    Button(buttons, text='Merge', command=multiple_pdf).grid(row=1, padx=40, pady=10)
    Button(buttons, text='Rotate', command=upload_rotation).grid(row=2, padx=40, pady=10)
    Button(buttons, text='Zoom In(+)', command=lambda: resize('increase')).grid(row=3, padx=30, pady=10)
    Button(buttons, text='Zoom Out(-)', command=lambda: resize('decrease')).grid(row=4, padx=30, pady=10)
    Button(buttons, text='Summary', command=print_summary).grid(row=5, padx=90, pady=10)

    # destroying the main window will close our application, instead we minimize it
    main_window.iconify()
    pdf_window.mainloop()


def main():
    Label(main_window, text=" ", font='Helvetica 18').place(relx=.5, rely=.5, anchor=CENTER)
    Button(main_window, text="Open File", background="white", foreground="red", font='Helvetica 13 bold',
           command=open_files).pack(
        pady=50)

    # executing the window
    main_window.mainloop()


if __name__ == '__main__':
    main()
