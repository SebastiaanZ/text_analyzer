"""
WordFrequencyAnalyzer analyzes word frequencies in a text.

Words are defined as sequences of characters in the set `[a-zA-Z]` and
separated by all characters not part of that set. This package comes
with two implementation styles:

- A modern idiomatic implementing
- An alternative Java-esque implementation using staticmethods

To use the alternative implementation, use `alternative.WordFrequencyAnalyzer`.
"""

from . import word_frequency_analyzer_alternative as alternative
from .word_frequency_analyzer import WordFrequency
from .word_frequency_analyzer import WordFrequencyAnalyzer


__all__ = [
    "WordFrequencyAnalyzer",
    "WordFrequency",
    "alternative",
]
__version__ = 1.0
