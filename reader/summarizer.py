from io import StringIO

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

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import textwrap

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')


# Extracts text from PDF using PDFMiner, accounts for column separation
def get_extracted_text(path):
    output_string = StringIO()

    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return output_string.getvalue()


def summarize(text):
    summary = ''
    stopword = set(
        stopwords.words("english"))  # Removes stopwords (a, the, and, in, etc.); separate one for punctuation also
    words = word_tokenize(text)
    freq_tabl = dict()  # Basically counts number of times a word is used in text
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

    # Splits extracted text into paragraphs by using double line breaks as a regex
    paragraphs = text.split("\n\n")

    # Cleans up sentences by removing line breaks, broken-line words
    sentences = []
    for paragraph in paragraphs:
        paragraph = paragraph.replace("\n", " ")
        paragraph = paragraph.replace("- ", "")
        paragraph = paragraph.replace("-\n", "")

        sents = sent_tokenize(paragraph)

        if len(sents) > 1:
            sentences += sents

    sent_tabl = dict()  # Gives a sentence a score based on the combined scores of words

    for sentence in sentences:  # Will also account for anytime a word/part of a word shows up in another sentence
        for word, freq in freq_tabl.items():
            if word in punctuation:
                continue
            if word in sentence.lower():
                if sentence in sent_tabl:
                    sent_tabl[sentence] += freq
                else:
                    sent_tabl[sentence] = freq

    sums = 0  # Sum = total added up sentence scores
    for sentence in sent_tabl:
        sums += sent_tabl[sentence]

    average = int(sums / len(sent_tabl))  # Gets average sentence score
    for sentence in sentences:  # Determines what will be put into the summary; above average = more importance
        if (sentence in sent_tabl) and (sent_tabl[sentence] > (
                3 * average)):  # Changing the value multiplied to average will narrow down the summary

            summary += "\n" + sentence

    # Returns summary as wrapped text for visual cleanliness
    return "\n".join(textwrap.wrap(summary, width=127))


def common_words_graph(text):  # Same as above, but this one will show a fancy graph
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
    fig = plt.figure(figsize=(7, 5))
    plt.gcf().subplots_adjust(bottom=0.15)
    fd = FreqDist(filtered)
    fd.plot(15, title='Commonly Used Terms', cumulative=False)
    fig.savefig('sdr_g.pdf', bbox_inches='tight')


def get_genre(text):  # Uses 20 Newsgroup dataset and Multinomial NB to predict
    genres = {  # a genre for the PDF file
        'alt.atheism': 'Atheism',  # Will print the predicted genre and the percentage of confidence
        'comp.graphics': 'Computer Graphics',  # in that prediction
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
    trainer = fetch_20newsgroups(subset='train', categories=genres.keys())

    count_vect = CountVectorizer()
    train_cv = count_vect.fit_transform(trainer.data)
    tfidf = TfidfTransformer()
    input_data = [text]
    train_tf = tfidf.fit_transform(train_cv)
    mnb_classifier = MultinomialNB().fit(train_tf, trainer.target)
    input_cv = count_vect.transform(input_data)
    input_tf = tfidf.transform(input_cv)
    prediction = mnb_classifier.predict(input_tf)

    predicted_category = ''
    for x, category in zip(input_data, prediction):
        predicted_category = 'Predicted Category: {}'.format(genres[trainer.target_names[category]])

    prob = mnb_classifier.predict_proba(input_tf)
    cat = int(prediction[0])
    value = round(prob.item(cat), 4) * 100
    confidence = 'Confidence: {}%'.format(value)

    return [predicted_category, confidence]


# Returns category prediction, confidence score, and summary in a list.
# [0][0] = prediction, [0][1] = score, [1] = summary
def get_summary(path):
    text = get_extracted_text(path)

    # Generates and saves common words graph

    summary = list()
    summary.append(get_genre(text))
    summary.append(summarize(text))

    return summary
