
import os
from tkinter import *
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf

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
