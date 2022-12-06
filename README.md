<h1>Clippy 🔎 </h3>


<h2 id="contents">Table of Contents</h2>
<ul>
  <li><span><a href=#about>About 💡</a>&ensp;</span></li>
  <li><span><a href=#how>How It Works 📖</a>&ensp;</span></li>
  <li><span><a href=#quickstart>Quickstart ⏩</a>&ensp;</span></li>
  <li><span><a href=#dependencies>Dependencies 📦</a>&ensp;</span></li>
  <li><span><a href=#installation>Installation ⚙️</a>&ensp;</span></li>
  <li><span><a href=#features>Features 🪴</a>&ensp;</span></li>
  <li><span><a href=#features>Future Plans 🔮</a>&ensp;</span></li>
  <li><span><a href=#features>Credits 📜</a>&ensp;</span></li>
</ul>

<br>
<br>
<h2 id=about>About 💡</h2>

> We decided to tackle this project because as college students, most of us will spend much of our time reading an abundance of documents. Using the guidelines, we thought it would be appropriate to create a Smart PDF reader so that when given a pdf or txt file, we are able to use features that help us understand the document to its full effect.

<br>

<h2 id=how>How It Works 📖</h2>

> Clippy takes a PDF and displays its contents, a summary, and its headings with a straightforward user interface.
> The summaries are generated using tokenization, count vectorization, TF-IDF, and Multinomial NB classification.
> The program also predicts the category of the given text
> (see [summarizer.py](https://github.com/jwc524/CLIPPY/blob/master/reader/summarizer.py) for more information).

<br>

<h2 id=quickstart>Quickstart ⏩</h2>

Using your preferred shell and the [Git CLI](https://cli.github.com/), the steps are as follows:

<br>

➊ Create and move to new directory.

```
mkdir clippy-clone
```

```
cd clippy-clone
```

<br>

➋ Clone repo using [Git CLI](https://cli.github.com/).

```
gh repo clone jwc524/clippy
```

<br>

<h2 id=dependencies>Dependencies 📦 </h2>
<ul>
  <li><a href=https://pypi.org/project/fpdf/ target="_blank" rel="noopener noreferrer" >fpdf</li>
  <li><a href=https://pypi.org/project/matplotlib/ target="_blank" rel="noopener noreferrer" >matplotlib</li>
  <li><a href=https://pypi.org/project/nltk/ target="_blank" rel="noopener noreferrer" >nltk</li>
  <li><a href=https://github.com/jsvine/pdfplumber/ target="_blank" rel="noopener noreferrer" >pdfplumber</li>
  <li><a href=https://pypi.org/project/pdfminer/ target="_blank" rel="noopener noreferrer" >pdfminer</li>
  <li><a href=https://pypi.org/project/PyMuPDF target="_blank" rel="noopener noreferrer" >pymupdf (requires version 1.18.17)</li>
  <li><a href=https://pypi.org/project/PyPDF2/ target="_blank" rel="noopener noreferrer" >pypdf2</li>
  <li><a href=https://pypi.org/project/sklearn/ target="_blank" rel="noopener noreferrer" >sklearn</li>
  <li><a href=https://pypi.org/project/ssl/>ssl</li>
  <li><a href=https://docs.python.org/3/library/textwrap.html>textwrap</li>
  <li><a href=https://docs.python.org/3/library/tkinter.html/ target="_blank" rel="noopener noreferrer"/>tkinter/ttk</li>
  <li><a href=https://pypi.org/project/tkPDFViewer/ target="_blank" rel="noopener noreferrer">tkpdfviewer</li>
</ul>

<br>

<h2 id=installation>Installation ⚙️ </h4>
<p>To install each dependency, use the following structure:</p>

```
pip install <package>
```

However, as mentioned in the [dependencies](#dependencies), *pymupdf* must be installed as such:

```
pip install pymupdf==1.18.17
```

<br>

For help with repository cloning, refer to [Quickstart ⏩](#quickstart).

<h2 id=features>Features 🪴 </h3>
<h6 id=headings>headings.py</h6>

> **Headings** parses the PDF for its headings and uses the document's outlines if they already exist. Primarily functions as a GUI class.

<h5 id=main>main.py</h5>

> **Main** is the bulk of the program, handling the user interface and calls to other functions.

<h5 id=merging>merging.py</h5>

> **Merging** handles the PDF merging calls from main.py. Primarily functions as a GUI class.

<h5 id=rotating>rotating.py</h5>

> **Rotating** handles PDF rotation as controlled by the user. Primarily functions as a GUI class.

<h5 id=summarizer>summarizer.py</h5>

> **Summarizer** parses the PDF and generates a summary using NLP methods. It also generates a number of graphs based on the extracted text.

<br>

<h2 id=future>Future Plans 🔮</h2>

Even though this project was created in a limited amount of time, there are some improvements to be made:
+ Creating a functional GUI
+ Improving the Data Mining Features
+ Implementing more user-friendly features
+ Extracting images and data tables for easy access

<h2 id=credits>Credits 📜</h2>

**This project was written by Ryan Truong, Tony Nguyen, and Jonathan Cole.**

<br>

<sub>This project was completed in fulfillment of the requirements of CSC 3400 at Belmont University. Special thank you to Dr. Esteban Parra Rodriguez.</sub>
