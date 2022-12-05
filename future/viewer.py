import os

from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import ttk
import pypdfium2 as pdfium
from PIL import Image, ImageTk
from tkinter import filedialog

from headings import get_headings


root = tk.Tk()
root.config(borderwidth=0, highlightthickness=0)

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

w1 = ws / 1.5
h = hs / 1.5

x = (ws/2) - (w1/2)
y = (hs/2) - (h/2)

scale_factor = 2
rotation = 0

root.geometry('%dx%d+%d+%d' % (w1, h, x, y))
root.title("PDF viewer")
root.configure(bg="white")

window = tk.Tk()
window.geometry('150x50+300+215')
window.title("Headings")
window.config(borderwidth=0, highlightthickness=0)

h = ttk.Scrollbar(root, orient="horizontal")
v = ttk.Scrollbar(root, orient="vertical")

w = tk.Tk()
w.geometry('120x50+1500+215')
w.title("Merge")

headings = {}


# Opens the PDF viewer from the given filepath.
def open_viewer(path):
    page_images = convert_to_img(path)
    headings = get_headings(path)
    reader = PdfReader(path)

    page_width = page_images[0].width()
    page_height = page_images[0].height()

    num_pages = reader.numPages
    total_height = page_height * num_pages

    cw = page_width / scale_factor
    ch = total_height

    btn = tk.Button(window, text="Print Headings", command=clicked)
    btn.grid(column=0, row=0, padx=30, pady=2)

    canvas = tk.Canvas(root,
                       width=cw,
                       height=ch,
                       scrollregion=(0, 0, cw, ch),
                       yscrollcommand=v.set,
                       xscrollcommand=h.set
                       )
    canvas.configure(borderwidth=0, highlightthickness=0)
    canvas.pack()

    h.config(command=canvas.xview)
    v.config(command=canvas.yview)

    canvas.grid(column=0, row=0, sticky="n, w, e, s")
    h.grid(column=0, row=1, sticky="w, e")
    v.grid(column=1, row=0, sticky="n, s")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    height_addition = 0
    for img in page_images:
        canvas.create_image(cw, height_addition, anchor="n", image=img)

        height_addition += page_height

    root.title(path)
    root.mainloop()


# browsing files through local directories to open files
def browse_files():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select PDF File",
                                          filetypes=(("PDF File", ".pdf"),
                                                     ("PDF File", ".PDF"),
                                                     ("All file", ".txt")))
    return filename


# Converts PDF pages to images using pypdfium2
def convert_to_img(path):
    pdf = pdfium.PdfDocument(path)
    images = []

    n_pages = len(pdf)
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        image = page.render_topil(
            scale=scale_factor,
            rotation=rotation,
            crop=(0, 0, 0, 0),
            greyscale=False,
            optimise_mode=pdfium.OptimiseMode.NONE,
        )

        image_tk = ImageTk.PhotoImage(image=image)

        images.append(image_tk)

    return images


def main():
    path = browse_files()
    open_viewer(path)

    root.mainloop()


def clicked():
    pass


if __name__ == '__main__':
    main()
