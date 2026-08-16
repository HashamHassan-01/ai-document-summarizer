# AI-Powered Document Summarization System

A command-line tool that summarizes text (typed, from `.txt`, or from `.pdf`) using extractive
summarization — it scores every sentence and keeps the top N.

> Teyzix Core Internship – Task AI-INT-1

## Features

- Load input from direct typing, a `.txt` file, or a `.pdf` file
- Three scoring methods:
  - **Frequency** – ranks sentences by how many high-frequency words they contain
  - **TF-IDF** – ranks sentences by term importance relative to the rest of the document
  - **Combined** – averages both (default, most accurate)
- Terminal analytics: top keywords with a bar chart, top-scoring sentences
- Export the summary as `.txt`, `.pdf`, or both

## Project Structure

```
.
├── main.py         # CLI entry point — run this
├── summarizer.py   # Core NLP logic (preprocessing, scoring, summary generation)
├── file_handler.py # Reading .txt/.pdf input, writing .txt/.pdf output
└── requirements.txt
```

## Setup

1. Clone the repo and enter it:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```
2. (Recommended) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

No manual NLTK setup is needed — `summarizer.py` automatically downloads the required
`punkt` and `stopwords` data the first time it runs.

## Usage

```bash
python main.py
```

You'll be prompted to:
1. Choose how to provide text (type it, load a `.txt`, or load a `.pdf`)
2. Choose how many sentences the summary should have
3. Choose a scoring method
4. Choose whether/how to save the output (`.txt`, `.pdf`, both, or neither)

## Example

```
How would you like to provide the text?
  1  Type / paste text directly
  2  Load from a .txt file
  3  Load from a .pdf file

Enter 1, 2, or 3: 2
Enter the path to your .txt file: article.txt

How many sentences in the summary? (default 3): 3
Choose scoring method:
  1 – Frequency
  2 – TF-IDF
  3 – Combined
Enter 1, 2, or 3: 3
```
