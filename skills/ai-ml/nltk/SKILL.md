---
name: nltk
description: Expert NLTK (Natural Language Toolkit) assistance covering tokenization, stemming, lemmatization, sentiment analysis, and POS tagging. Use when preprocessing text corpora and classical NLP tasks.
---

# NLTK

NLTK is the classic library for teaching and researching NLP. While slower than spaCy, it offers **comprehensive** linguistic data.

## When to Use

- **Classical NLP & Linguistics**: Tokenization, stemming, lemmatization, part-of-speech (POS) tagging, and syntactic parsing.
- **Rule-Based Sentiment Analysis**: Quick heuristic sentiment scoring with VADER for social media texts.
- **Text Preprocessing for Classical ML**: Cleaning corpus text for TF-IDF, Naive Bayes, and SVM models.
- **Educational & Linguistic Research**: Analyzing word frequencies, collocations, and lexical dispersion across corpora.

## Quick Start

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt_tab')
nltk.download('stopwords')

text = "Natural Language Toolkit provides classical algorithms for text analysis."
tokens = word_tokenize(text)
stop_words = set(stopwords.words('english'))
filtered = [w for w in tokens if w.lower() not in stop_words and w.isalnum()]

print("Filtered tokens:", filtered)
```

## Core Concepts

#Tokenization, Stopwords & WordNet Lemmatization

Standard text normalization pipeline:

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Ensure required corpora are downloaded
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_text(raw_text: str) -> list[str]:
    # 1. Lowercase and tokenize
    tokens = word_tokenize(raw_text.lower())

    # 2. Filter punctuation and English stopwords
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in tokens if w.isalnum() and w not in stop_words]

    # 3. Lemmatize words to base dictionary form
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w) for w in filtered]

    return lemmatized

sample = "The distributed microservices were running exceptionally fast and scaling reliably!"
print("Cleaned Tokens:", preprocess_text(sample))
```

#VADER Sentiment Analysis for Fast Heuristic Scoring

Rule-based sentiment intensity scoring:

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

reviews = [
    "Antigravity IDE is amazingly responsive and saves hours of tedious refactoring!",
    "The legacy codebase crashes constantly with unhelpful error messages.",
    "The software was delivered on Tuesday afternoon."
]

for review in reviews:
    scores = sia.polarity_scores(review)
    compound = scores['compound']
    sentiment = 'positive' if compound >= 0.05 else ('negative' if compound <= -0.05 else 'neutral')
    print(f"Sentiment: {sentiment:8s} (Score: {compound:+.2f}) | {review[:50]}...")
```

#Part-of-Speech (POS) Tagging & Named Entity Chunking

Extracting grammatical structures from text:

```python
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('maxent_ne_chunker_tab', quiet=True)
nltk.download('words', quiet=True)

sentence = "Sundar Pichai announced new Gemini models at Google headquarters."
tokens = word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens)

# Extract named entities
chunks = nltk.ne_chunk(pos_tags)
for chunk in chunks:
    if hasattr(chunk, 'label'):
        print(f"Entity: {' '.join(c[0] for c in chunk)} [{chunk.label()}]")
```

## Common Patterns

### Lemmatization with POS (Part of Speech) Tagging

**Problem**: Simple stemmers truncate words unnaturally (`running` -> `run`, but `better` -> `better`).

**Solution**:
Combine WordNetLemmatizer with POS tags:

```python
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
# Lemmatize with explicit verb POS tag
print(lemmatizer.lemmatize("running", wordnet.VERB)) # Output: run
print(lemmatizer.lemmatize("better", wordnet.ADJ))   # Output: good
```

## Best Practices (2026)

- **Do** prefer lemmatization over stemming (`PorterStemmer`) for human-readable root words.
- **Do** download specific corpora explicitly in setup scripts (`nltk.download('punkt_tab')`) to prevent runtime failures in Docker.
- **Do** leverage VADER for social media text where punctuation and capitalization convey sentiment.
- **Do** migrate to spaCy or Hugging Face transformers when semantic understanding or modern deep learning is required.
- **Don't** call `nltk.download()` repeatedly on every request inside web handlers; download once at build/container time.
- **Don't** use NLTK for high-throughput production tokenization; use Hugging Face tokenizers or spaCy.
- **Don't** use WordNet lemmatizer without specifying POS tags if fine-grained verb/noun distinction is needed.

## Troubleshooting

| Error                                   | Cause                                                               | Solution                                                              |
| :-------------------------------------- | :------------------------------------------------------------------ | :-------------------------------------------------------------------- |
| `Resource punkt_tab not found`          | Required NLTK dataset not downloaded locally.                       | Add `nltk.download('punkt_tab')` before tokenization call.            |
| `LookupError: WordNet resource missing` | WordNet database not installed.                                     | Execute `nltk.download('wordnet')`.                                   |
| `Slow tokenization on massive text`     | NLTK regex tokenizers running single-threaded on millions of lines. | Batch processing with multiprocessing or use Hugging Face tokenizers. |

## References

- [NLTK Documentation](https://www.nltk.org/)
