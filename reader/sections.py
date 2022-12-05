# src: https://stackoverflow.com/questions/70170544/pdfplumber-extract-text-from-dynamic-column-layouts

from io import StringIO

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def convert_pdf_to_string(file_path):
    output_string = StringIO()

    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return output_string.getvalue()


file_path = r'../pdfs/BURT.pdf'  # !
text = convert_pdf_to_string(file_path)

sections = {}

# Splits extracted text into paragraphs
paragraphs = text.split('\n\n')

sentences_list = list()
for paragraph in paragraphs:
    sentences = sent_tokenize(paragraph)

    for sentence in sentences:
        # sentence = sentence.replace('\n', ' ')  # Removes line breaks
        # sentence = sentence.replace('- ', '')   # Removes end-of-line breaks

        sentences.append(sentence)

    sentences_list.append(sentences)

for sentence in sentences_list:
    print(sentence)