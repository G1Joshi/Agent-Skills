---
name: spacy
description: Expert spaCy assistance covering industrial NLP, NER (Named Entity Recognition), rule-based matching, dependency parsing, and pipelines. Use when building production-grade information extraction pipelines.
---

# spaCy

spaCy is "Industrial Strength" NLP. Unlike NLTK (academic), spaCy focuses on providing the **best** single algorithm for a task. v3.8 supports Python 3.13.

## When to Use

- **Production-Ready Natural Language Processing**: Fast, industrial-grade tokenization, lemmatization, and dependency parsing.
- **Named Entity Recognition (NER)**: Extracting organizations, people, locations, dates, and domain-specific entities.
- **Rule-Based Matching & Pattern Extraction**: Combining linguistic rules with regex and token attributes using `Matcher` and `EntityRuler`.
- **Large-Scale Text Processing Pipelines**: Batch processing millions of documents with `nlp.pipe()` and GPU acceleration.

## Quick Start

```python
import spacy

# Load transformer or core English pipeline
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is acquiring a London startup for $1 billion.")

# Extract named entities
for ent in doc.ents:
    print(f"{ent.text:<15} {ent.label_:<10}")
# Output:
# Apple           ORG
# London          GPE
# $1 billion      MONEY
```

## Core Concepts

### High-Throughput Batch Processing with nlp.pipe

Processing document streams efficiently using multiprocessing and batching:

```python
import spacy

# Load transformer or optimized small model
nlp = spacy.load("en_core_web_sm")

documents = [
    "Apple Inc. acquired a machine learning startup based in Zurich for $200 million.",
    "Dr. Maria Santos published research on genomic sequencing at Oxford University.",
    "Amazon Web Services launched new European cloud regions in Frankfurt."
]

# Process documents in batches, disabling unused pipeline stages
for doc in nlp.pipe(documents, batch_size=64, disable=["parser"]):
    print(f"--- Document ({len(doc)} tokens) ---")
    for ent in doc.ents:
        print(f"Entity: {ent.text:25s} Label: {ent.label_}")
```

### Rule-Based EntityRuler & Pattern Matching

Combining custom dictionary rules with statistical NER:

```python
nlp = spacy.load("en_core_web_sm")

# Add EntityRuler before the statistical ner component
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "PRODUCT_SKU", "pattern": [{"TEXT": {"REGEX": r"^SKU-\d{4}-[A-Z]{2}$"}}]},
    {"label": "SECURITY_FLAG", "pattern": [{"LOWER": "unauthorized"}, {"LOWER": "access"}]}
]
ruler.add_patterns(patterns)

doc = nlp("Alert: unauthorized access detected for asset SKU-8492-EU on production server.")
for ent in doc.ents:
    print(f"Match: {ent.text} -> {ent.label_}")
```

### Syntactic Dependency Parsing & Semantic Traversal

Extracting subject-verb-object relationships:

```python
doc = nlp("Autonomous vehicles navigate complex city intersections safely.")

for token in doc:
    print(f"{token.text:12s} Dep: {token.dep_:10s} Head: {token.head.text:12s} POS: {token.pos_}")

# Extract grammatical subject and direct object
for token in doc:
    if "subj" in token.dep_:
        print(f"Subject: {token.text}")
    elif "obj" in token.dep_:
        print(f"Object: {token.text}")
```

## Common Patterns

### Efficient Batch Processing with nlp.pipe

**Problem**: Calling `nlp(text)` one by one on millions of records is slow and underutilizes CPU cores.

**Solution**:
Process text in batches with disabled unused pipeline components:

```python
texts = ["Invoice #1234 from Vendor A...", "Contract dated 2025..."]

# Disable tagger and parser if only NER is required
for doc in nlp.pipe(texts, batch_size=50, disable=["tagger", "parser"]):
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(entities)
```

## Best Practices

**Do**:

- Always use `nlp.pipe(texts, batch_size=...)` instead of iterating with `[nlp(t) for t in texts]`.
- Disable pipeline components not required for the task (`nlp.pipe(texts, disable=["parser", "ner"])`) to gain up to 5x speedups.
- Call `spacy.require_gpu()` before loading models when running on CUDA-enabled servers.
- Train custom spaCy components using the declarative `config.cfg` system and `spacy train`.

**Don't**:

- Load the heavy transformer model (`en_core_web_trf`) if simple tokenization/POS with `en_core_web_sm` suffices.
- Modify `doc.ents` directly without handling token boundary overlaps; use `spacy.util.filter_spans`.
- Reload `spacy.load()` inside request handlers; load models once as global singletons.

## Troubleshooting

| Error                                                             | Cause                                                           | Solution                                                            |
| :---------------------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------ |
| `Can't find model 'en_core_web_sm'`                               | Model weights package not downloaded.                           | Run `python -m spacy download en_core_web_sm`.                      |
| `ValueError: [E088] Text of length ... exceeds maximum`           | Input text exceeds default maximum character limit (1,000,000). | Increase limit: `nlp.max_length = 2000000` or chunk long documents. |
| `UserWarning: [W036] The component '...' does not have attribute` | Pipeline component ordering incorrect during custom extension.  | Inspect pipeline order with `nlp.pipe_names`.                       |

## References

- [spaCy Documentation](https://spacy.io/)
