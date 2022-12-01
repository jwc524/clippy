import os
import pdfplumber
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#replace 'example.pdf' with name of another file
with pdfplumber.open(r'example.pdf') as pdf:
    extracted_page = pdf.pages[0]
    extracted_text = extracted_page.extract_text()

def summarize(text):
    stopword = set(stopwords.words("english"))                   # Removes stopwords (a, the, and, in, etc.)
    words = word_tokenize(text)                         # Word tokenizer for tokenizing
    freq_tabl = dict()                                            # Frequency table uses dictionary to track most commonly used words excluding all stopwords
    for word in words:                                            
        word = word.lower()
        if word in stopword:
            continue
        if word in freq_tabl:
            freq_tabl[word] += 1
        else:
            freq_tabl[word] = 1

    sentences = sent_tokenize(text)                     # Functions like word tokenizer, but now applies for full sentences
    sent_tabl = dict()                                            # Similar to frequency table
    for sentence in sentences:
        for word, freq in freq_tabl.items():
            if word in sentence.lower():
                if sentence in sent_tabl:
                    sent_tabl[sentence] += freq
                else:
                    sent_tabl[sentence] = freq

    sum = 0                                                       # This and the following for loop are used to score sentences based on a perceived
    for sentence in sent_tabl:                                    # importance that comes from how frequently the words in the sentence pops up elsewhere
        sum += sent_tabl[sentence]

    average = int(sum / len(sent_tabl))                             # Average score of a sentence is used to determine what is used in the summary
    summary = ''
    for sentence in sentences:
        if (sentence in sent_tabl) and (sent_tabl[sentence] > (1.2 * average)):
            summary += " " + sentence
    
    return summary

print(summarize(extracted_text))
