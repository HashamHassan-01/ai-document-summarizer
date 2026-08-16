# ============================================================
#  summarizer.py  –  Core summarization logic
# ============================================================
# This file contains all the NLP functions:
#   1. Text preprocessing (clean the raw text)
#   2. Word frequency scoring
#   3. TF-IDF scoring
#   4. Sentence ranking & summary generation
# ============================================================

import re
from collections import Counter

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# ── 0. NLTK DATA SETUP ──────────────────────────────────────
# NLTK needs a couple of small data packages (sentence/word tokenizer models
# and the English stopword list) that are NOT included with the library
# itself. Without this, sent_tokenize/word_tokenize/stopwords all raise a
# LookupError on any machine that hasn't manually run nltk.download() before.
# This checks for each package and silently fetches it once if missing, so
# the script works out of the box after `pip install -r requirements.txt`.

def _ensure_nltk_data():
    required = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),   # needed by nltk >= 3.8.2
        ("corpora/stopwords", "stopwords"),
    ]
    for find_path, package_name in required:
        try:
            nltk.data.find(find_path)
        except LookupError:
            try:
                nltk.download(package_name, quiet=True)
            except Exception:
                # e.g. punkt_tab doesn't exist on older nltk versions — ignore
                pass


_ensure_nltk_data()


# ── 1. PREPROCESSING ────────────────────────────────────────

def preprocess_text(text):
    """
    Clean raw text before scoring.
    Steps:
      - lowercase everything
      - remove non-letter characters (punctuation, numbers)
      - tokenize into words
      - remove stopwords (the, is, a, ...)
    Returns a list of clean words.
    """
    # Lowercase
    text_lower = text.lower()

    # Keep only letters and spaces
    text_clean = re.sub(r"[^a-z\s]", "", text_lower)

    # Split into individual words (tokenize)
    words = word_tokenize(text_clean)

    # Load English stopwords and remove them
    stop_words = set(stopwords.words("english"))
    filtered_words = [w for w in words if w not in stop_words and len(w) > 1]

    return filtered_words


def split_into_sentences(text):
    """
    Split the full text into a list of sentences.
    Example: "Hello world. How are you?" → ["Hello world.", "How are you?"]
    """
    sentences = sent_tokenize(text)
    # Remove very short sentences (less than 5 words) – they carry little info
    sentences = [s for s in sentences if len(s.split()) >= 5]
    return sentences


# ── 2. FREQUENCY-BASED SCORING ──────────────────────────────

def frequency_score_sentences(sentences, filtered_words):
    """
    Score each sentence based on how many important (frequent) words it contains.

    Logic:
      - Count how often each word appears in the whole document
      - For each sentence, add up the counts of its words
      - Higher total = more important sentence
    """
    # Count frequency of each word
    word_freq = Counter(filtered_words)

    sentence_scores = {}

    for sentence in sentences:
        # Clean each sentence the same way before scoring
        words_in_sentence = word_tokenize(sentence.lower())
        score = 0
        for word in words_in_sentence:
            if word in word_freq:
                score += word_freq[word]
        sentence_scores[sentence] = score

    return sentence_scores


# ── 3. TF-IDF SCORING ───────────────────────────────────────

def tfidf_score_sentences(sentences):
    """
    Score sentences using TF-IDF (smarter than plain frequency).

    TF  = how often a word appears in THIS sentence
    IDF = penalizes words that appear in EVERY sentence (so they're not special)
    TF-IDF = TF × IDF  →  words that are frequent HERE but rare ELSEWHERE score high

    Returns a score per sentence (sum of its TF-IDF values).
    """
    if len(sentences) < 2:
        # TF-IDF needs at least 2 sentences to compare
        return {s: 1 for s in sentences}

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Sum TF-IDF scores across all words in each sentence
    sentence_scores = {}
    scores_array = np.array(tfidf_matrix.sum(axis=1)).flatten()

    for i, sentence in enumerate(sentences):
        sentence_scores[sentence] = float(scores_array[i])

    return sentence_scores


# ── 4. COMBINED SCORING & SUMMARY ───────────────────────────

def rank_sentences(sentences, filtered_words, method="combined"):
    """
    Rank sentences by importance using the chosen method.

    method options:
      "frequency" – use word frequency scoring only
      "tfidf"     – use TF-IDF scoring only
      "combined"  – average of both (most accurate)
    """
    freq_scores  = frequency_score_sentences(sentences, filtered_words)
    tfidf_scores = tfidf_score_sentences(sentences)

    ranked = {}
    for sentence in sentences:
        if method == "frequency":
            ranked[sentence] = freq_scores.get(sentence, 0)
        elif method == "tfidf":
            ranked[sentence] = tfidf_scores.get(sentence, 0)
        else:  # combined
            # Normalize each score to 0-1 range then average them
            ranked[sentence] = (freq_scores.get(sentence, 0) + tfidf_scores.get(sentence, 0)) / 2

    return ranked


def generate_summary(text, num_sentences=3, method="combined"):
    """
    Full pipeline: raw text → clean → score → pick top sentences → summary.

    Parameters:
      text          – the input document as a string
      num_sentences – how many sentences to include in the summary
      method        – scoring method: "frequency", "tfidf", or "combined"

    Returns:
      summary       – the generated summary string
      sentences     – all sentences found in the text
      scores        – importance score for each sentence
    """
    # Step 1 – split text into sentences (keep original for output)
    sentences = split_into_sentences(text)

    if not sentences:
        return "No sentences found in the text.", [], {}

    # Cap num_sentences so we don't ask for more than exist
    num_sentences = min(num_sentences, len(sentences))

    # Step 2 – preprocess for scoring
    filtered_words = preprocess_text(text)

    # Step 3 – score every sentence
    scores = rank_sentences(sentences, filtered_words, method)

    # Step 4 – pick top N sentences
    top_sentences = sorted(scores, key=scores.get, reverse=True)[:num_sentences]

    # Step 5 – put them back in the original order (so summary reads naturally)
    summary_sentences = [s for s in sentences if s in top_sentences]
    summary = " ".join(summary_sentences)

    return summary, sentences, scores


# ── 5. ANALYTICS ────────────────────────────────────────────

def get_top_keywords(filtered_words, top_n=10):
    """Return the top N most frequent words (keywords)."""
    word_freq = Counter(filtered_words)
    return word_freq.most_common(top_n)


def get_word_frequency(filtered_words):
    """Return full word frequency dictionary."""
    return dict(Counter(filtered_words))
