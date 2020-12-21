"""
A Java-esque implementation of the WordFrequencyAnalyzer.

This is an alternative implementation of the assignment tha more
closely follows the specified interface/class API. However, this
leads to patterns that are fairly uncommon or even generally
considered to be anti-patterns in modern Python applications.

The main difference with the specification here is that, in Python,
"getter"-methods are typically implemented using properties. This
means that there are no `get_word` or `get_frequency` methods in the
WordFrequency class, but rather properties that serve the same purpose
but follow the "uniform access principle" (as defined by Betrand Meyer
in "Object-Oriented Software Construction", 1988, 1997).
"""
__all__ = [
    "WordFrequency",
    "WordFrequencyAnalyzer",
]

import collections
import re


class WordFrequency:
    """
    A class that represents the frequency of a word in a text.

    Constructor arguments:
    word (str)      -- the word the frequency belongs to
    frequency (int) -- the frequency that belongs to the word
    """

    def __init__(self, word: str, frequency: int) -> None:
        self._word = word
        self._frequency = frequency

    @property
    def word(self) -> str:
        """Get the value of `word` for this WordFrequency pair."""
        return self._word

    @property
    def frequency(self) -> int:
        """Get the value of `frequency` for this WordFrequency pair."""
        return self._frequency


class WordFrequencyAnalyzer:
    """
    A frequency analyzer that analyzes a text for word frequencies.

    For this analyzer, words are considered to be sequences of
    alphabetic characters that are uninterrupted by non-alphabetic
    characters. The case of letters will be ignored ignored.
    """

    @staticmethod
    def _word_frequencies(text: str) -> collections.Counter[str, int]:
        """Calculate the frequency for each word in the text."""
        return collections.Counter(re.findall(r"[a-z]+", text.lower()))
