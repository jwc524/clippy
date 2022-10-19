import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

file_name = "Desktop/smart pdf reader/example.pdf"

fd =  open(file_name, "rb")
viewer = SimplePDFViewer(fd)

for canvas in viewer:
    page_img = canvas.images
    page_forms = canvas.forms
    page_txt = canvas.text_content
    page_inline_img = canvas.inline_images
    page_strings = canvas.strings

viewer.navigate(1)
viewer.render()
print(viewer.canvas.strings)
##viewer.canvas.text_content
