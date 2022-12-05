import os
import pdfplumber
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')

#replace 'example.pdf' with name of another file
with pdfplumber.open(r'../pdfs/BURT.pdf') as pdf:
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
        if (sentence in sent_tabl) and (sent_tabl[sentence] > (1.465 * average)):   # Changing the value multiplied to average will narrow down the summary
            summary += " " + sentence
    
    return summary

def common_words(text):
    stopword = set(stopwords.words('english'))              # Will display the 15 most commonly used terms in the file
    words = word_tokenize(text)
    filtered = []
    for word in words:
        word = word.lower()
        if word in stopword:
            continue
        if word in punctuation:
            continue
        else:
            filtered.append(word)
    fd = FreqDist(filtered)
    return fd.most_common(15)

def common_words_graph(text):                               # Same as above, but this one will show a fancy graph
    stopword = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered = []
    for word in words:
        word = word.lower()
        if word in stopword:
            continue
        if word in punctuation:
            continue
        else:
            filtered.append(word)
    fig = plt.figure(figsize = (7, 5))
    plt.gcf().subplots_adjust(bottom = 0.15)
    fd = FreqDist(filtered)
    fd.plot(15, title = 'Commonly Used Terms', cumulative = False)
    fig.savefig('sdr_g.pdf', bbox_inches = 'tight')

def get_genre(text):                                        # Uses 20 Newsgroup dataset and Multinomial NB to predict
    genres = {                                              # a genre for the PDF file
        'alt.atheism': 'Atheism',
        'comp.graphics': 'Computer Graphics',
        'comp.os.ms-windows.misc': 'Microsoft Windows',
        'comp.sys.ibm.pc.hardware': 'PC Hardware',
        'comp.sys.mac.hardware': 'Mac Hardware',
        'misc.forsale': 'Commericial/Promotion',
        'rec.autos': 'Automobiles',
        'rec.sport.baseball': 'Baseball',
        'rec.sport.hockey': 'Hockey',
        'sci.crypt': 'Cryptocurrency or Cryptozoology',
        'sci.electronics': 'Electronics',
        'sci.med': 'Medicine',
        'sci.space': 'Space',
        'soc.religion.christian': 'Christianity',
        'talk.politics.guns': 'Gun Laws',
        'talk.politics.mideast': 'Mideast Conflict',
        'talk.politics.misc': 'Politics',
        'talk.religion.misc': 'Religion'
    }
    trainer = fetch_20newsgroups(subset = 'train', categories = genres.keys())

    count_vect = CountVectorizer()
    train_cv = count_vect.fit_transform(trainer.data)
    tfidf = TfidfTransformer()
    input_data = [text]
    train_tf = tfidf.fit_transform(train_cv)
    mnb_classifier = MultinomialNB().fit(train_tf, trainer.target)
    input_cv = count_vect.transform(input_data)
    input_tf = tfidf.transform(input_cv)
    prediction = mnb_classifier.predict(input_tf)
    
    for x, category in zip(input_data, prediction):
        print('\nPredicted category:',
            genres[trainer.target_names[category]])


# print(extracted_text)
print("\n     Summary:")
print(summarize(extracted_text))
# print("\nCommon words:")
# print(common_words(extracted_text))
# print(punctuation)
get_genre(extracted_text)
common_words_graph(extracted_text)
