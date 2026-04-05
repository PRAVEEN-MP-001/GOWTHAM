"""
Lightweight matching engine (no PyTorch / sentence-transformers):
  Final Score = 0.5 × tfidf_score + 0.5 × bigram_score

tfidf_score  — TF-IDF cosine similarity (unigrams, scikit-learn)
bigram_score — TF-IDF cosine similarity (bigrams, scikit-learn)

Using two n-gram levels approximates some of the phrase-awareness that
sentence-transformers provides, without the ~2.5 GB PyTorch dependency.
"""
from __future__ import annotations

import logging
from typing import Tuple

import numpy as np  # type: ignore[import]
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[import]
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore[import]

logger = logging.getLogger(__name__)


def _tfidf_cosine(text_a: str, text_b: str, ngram_range: tuple = (1, 1)) -> float:
    """TF-IDF cosine similarity for a given n-gram range."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=ngram_range)
    try:
        matrix = vectorizer.fit_transform([text_a, text_b])
        score = cosine_similarity(matrix[0], matrix[1])[0][0]
        return float(np.clip(score, 0.0, 1.0))
    except Exception:
        return 0.0


def _keyword_score(text_a: str, text_b: str) -> float:
    """Unigram TF-IDF cosine similarity."""
    return _tfidf_cosine(text_a, text_b, ngram_range=(1, 1))


def _phrase_score(text_a: str, text_b: str) -> float:
    """Bigram TF-IDF cosine similarity — captures phrase-level overlap."""
    return _tfidf_cosine(text_a, text_b, ngram_range=(2, 2))


def compute_match_score(resume_text: str, job_description: str) -> Tuple[float, float, float]:
    """
    Returns (final_score, keyword_score, phrase_score) all in [0, 1].
    Final formula: 0.5 × unigram + 0.5 × bigram
    """
    kw = _keyword_score(resume_text, job_description)
    ph = _phrase_score(resume_text, job_description)
    final = 0.5 * kw + 0.5 * ph
    return round(float(final), 4), round(float(kw), 4), round(float(ph), 4)  # type: ignore[call-overload]
