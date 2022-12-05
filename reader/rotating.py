import PyPDF2


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
