import os
import pdfplumber
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#needs to be turned into a def

#replace 'example.pdf' with name of another file
with pdfplumber.open(r'example.pdf') as pdf:
    extracted_page = pdf.pages[0]
    extracted_text = extracted_page.extract_text()

#turn line 13 to 46 into methods
stopwords = set(stopwords.words("english"))
words = word_tokenize(extracted_text)
frequency_table = dict()
for word in words:
    word = word.lower()
    if word in stopwords:
        continue
    if word in frequency_table:
        frequency_table[word] += 1
    else:
        frequency_table[word] = 1

sentences = sent_tokenize(extracted_text)
sentence_value = dict()
for sentence in sentences:
    for word, freq in frequency_table.items():
        if word in sentence.lower():
            if sentence in sentence_value:
                sentence_value[sentence] += freq
            else:
                sentence_value[sentence] = freq

sum_value = 0
for sentence in sentence_value:
    sum_value += sentence_value[sentence]

average = int(sum_value/len(sentence_value))
summary = ''
for sentence in sentences:
    if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * average)):
        summary += " " + sentence

print(summary)