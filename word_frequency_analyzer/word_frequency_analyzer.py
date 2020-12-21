"""
A modern implementation of the WordFrequencyAnalyzer.

This file contains a modern implementation of the WordFrequencyAnalyzer
written in Python 3.9.

While the resulting class API is slightly different from the specified
interface in the assignment, it uses patterns more commonly found in
modern Python applications.

An implementation using an API that matches the specification can be
found in `word_frequency_analyzer_alternative.py`.
"""
import collections
import functools
import re
import typing

__all__ = [
    "WordFrequency",
    "WordFrequencyAnalyzer",
]


class WordFrequency(typing.NamedTuple):
    """A NamedTuple that represents a word and its frequency."""

    word: str
    frequency: int


class WordFrequencyAnalyzer:
    """
    A frequency analyzer that analyzes a text for word frequencies.

    For this analyzer, words are considered to be sequences of
    alphabetic characters. All other characters will be interpreted
    as the separation between words.

    This analyzer calculates the case insensitive frequency.
    """

    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self) -> str:
        """
        Return the official representation of an instance.

        Following the guidelines in the documentation for
        object.__repr__, the representation is wrapped in angle
        brackets to indicate that it's potentially only a partial
        representation of the object.
        """
        cls_name = type(self).__name__
        short_text = f"{self.text:29.29}..." if len(self.text) > 32 else self.text
        return f"<{cls_name} text={short_text!r}>"

    @functools.cached_property
    def word_frequencies(self) -> collections.Counter[str, int]:
        """
        Get the frequency of each word in the text.

        Word frequencies are lazily computed: The text will be analyzed
        the first time this attribute is accessed and the result will be
        cached for subsequent attribute look-ups.
        """
        return collections.Counter(re.findall(r"[a-z]+", self.text.lower()))

    def calculate_highest_frequency(self) -> int:
        """Calculate the highest word frequency in the text."""
        if not self.word_frequencies:
            # If the text did not contain any words, return `0`.
            return 0

        [(_word, frequency)] = self.word_frequencies.most_common(1)
        return frequency

    def calculate_frequency_for_word(self, word: str) -> int:
        """Return the frequency of the given word."""
        return self.word_frequencies[word.lower()]

    def calculate_most_frequent_n_words(self, n: int) -> list[WordFrequency]:
        """
        Return the most frequent `n` words in the text.

        This method returns a list of WordFrequency tuples and uses
        ascending alphabetical order in the case of ties.
        """
        if n < 0:
            raise ValueError("requested word count `n` cannot be negative.")

        # Sort the (word, frequency) pairs primarily by frequency, and
        # secondarily by their alphabetic order.
        sorted_words = sorted(self.word_frequencies.items(), key=lambda item: (-item[1], item[0]))
        return [WordFrequency(word, frequency) for word, frequency in sorted_words[:n]]
