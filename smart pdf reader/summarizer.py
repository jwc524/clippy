import os
import pdfplumber
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation 

#replace 'example.pdf' with name of another file
with pdfplumber.open(r'example.pdf') as pdf:
    extracted_page = pdf.pages[0]
    extracted_text = extracted_page.extract_text(x_tolerance = 1)      # x_tolerance is default to 3; changing to one removes tendency for it to group together
                                                                       # multiple words due to a new line
def summarize(text):
    summary = ''                                                  
    stopword = set(stopwords.words("english"))                         # Removes stopwords (a, the, and, in, etc.); separate one for puncuation also
    words = word_tokenize(text)                                        
    freq_tabl = dict()                                                 # Basically counts number of times a word is used in text
    for word in words:                                                 
        word = word.lower()
        if word in stopword:
            continue
        if word in punctuation:
            continue
        if word in freq_tabl:
            freq_tabl[word] += 1
        else:
            freq_tabl[word] = 1

    sentences = sent_tokenize(text)                               
    sent_tabl = dict()                                            # Gives a sentence a score based on the combined scores of words
    for sentence in sentences:                                    # Will also account for anytime a word/part of a word shows up in another sentence
        for word, freq in freq_tabl.items():
            if word in punctuation:
                continue
            if word in sentence.lower():
                if sentence in sent_tabl:
                    sent_tabl[sentence] += freq
                else:
                    sent_tabl[sentence] = freq 

    sum = 0                                                       # Sum = total added up sentence scores
    for sentence in sent_tabl:      
        sum += sent_tabl[sentence]

    average = int(sum / len(sent_tabl))                                              # Gets average sentence score
    for sentence in sentences:                                                       # Determines what will be put into the summary; above average = more importance
        if (sentence in sent_tabl) and (sent_tabl[sentence] > (1.4625 * average)):   # Changing the value multiplied to average will narrow down the summary
            summary += " " + sentence                                                
    
    return summary

def common_words(text):
    stopword = set(stopwords.words("english"))                    # Basically that first section of 'summarize'
    words = word_tokenize(text)                                   # Now used to return the most common words used in text  
    freq_tabl = dict()                                            
    for word in words:                                            
        word = word.lower()
        if word in stopword:
            continue
        if word in punctuation:
            continue
        if word in freq_tabl:
            freq_tabl[word] += 1
        else:
            freq_tabl[word] = 1

    sorted_tabl = dict(sorted(freq_tabl.items(), key = lambda item: item[1], reverse = True))
    return sorted_tabl

    #return freq_tabl

#print(extracted_text)
#print("\n     Summary:")
#print(summarize(extracted_text))
#print("\nCommon words:")
#print(common_words(extracted_text))
#print(punctuation)
