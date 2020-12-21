import collections
import random
import string
import unittest

from hypothesis import given
from hypothesis.strategies import characters, composite, dictionaries, integers, lists, text

from word_frequency_analyzer import WordFrequency, WordFrequencyAnalyzer


WORD_ALPHABET = characters(whitelist_categories=(), whitelist_characters=string.ascii_letters)
WORD = text(alphabet=WORD_ALPHABET, min_size=1, max_size=12)

SEPARATOR_CHARACTERS = string.punctuation + string.whitespace
SEPARATOR_ALPHABET = characters(whitelist_categories=(), whitelist_characters=SEPARATOR_CHARACTERS)
SEPARATOR = text(alphabet=SEPARATOR_ALPHABET, min_size=1, max_size=4)


def expand_words_from_counts(word_counts: dict[str, int]) -> tuple[dict[str, int], list[str]]:
    """Expand words using their counts to a list of words in randomized order."""
    expanded_words = [word for word, count in word_counts.items() for _ in range(count)]
    random.shuffle(expanded_words)

    # We need the case insensitive counts to compare against.
    case_insensitive_counts = collections.defaultdict(int)
    for word, count in word_counts.items():
        case_insensitive_counts[word.lower()] += count

    return case_insensitive_counts, expanded_words


@composite
def generate_words_with_random_separators(draw):
    """Generate words with known counts separated by random whitespace/punctuation characters."""
    word_counts = draw(dictionaries(keys=WORD, values=integers(min_value=1, max_value=50)))
    case_insensitive_counts, expanded_words = expand_words_from_counts(word_counts)

    # Mix the words with random separators
    words_with_separators = []
    for word in expanded_words:
        words_with_separators.append(word)
        words_with_separators.append(draw(SEPARATOR))

    return "".join(words_with_separators), case_insensitive_counts


@composite
def generate_text_known_most_common_word_frequency(draw):
    """Generate a text with a known most common word frequency."""
    words = draw(lists(WORD, unique_by=str.lower))
    frequency_most_common = draw(integers(min_value=2, max_value=50)) if words else 0

    expanded_words = words[:1] * frequency_most_common
    for word in words[1:]:
        expanded_words += [word] * draw(integers(min_value=1, max_value=frequency_most_common))

    random.shuffle(expanded_words)
    return " ".join(expanded_words), frequency_most_common


@composite
def generate_words_with_random_frequencies(draw):
    """Generate text with randomized word frequencies."""
    word_counts = draw(dictionaries(keys=WORD, values=integers(min_value=0, max_value=50)))
    case_insensitive_counts, expanded_words = expand_words_from_counts(word_counts)
    return " ".join(expanded_words), case_insensitive_counts


class WordFrequencyInvariantsTests(unittest.TestCase):
    """
    Use property-based testing to test the frequency analysis.

    Instead of testing the frequency logic against just a few scenarios
    this test case uses `hypothesis` to generate test cases for a wide
    range of scenarios.

    The WordFrequencyAnalyzer is tested against these invariants:

    - WordFrequencyAnalyzer.word_frequencies should always return a
      Counter instance as long as a valid utf-8 string is passed.

    - WordFrequencyAnalyzer.word_frequencies should always return the
      correct word counts for text with any kind of valid words.

    - WordFrequencyAnalyzer.calculate_highest_frequency should always
      return the highest frequency regardless of other words.

    - WordFrequencyAnalyzer.calculate_frequency_for_word should always
      return the count for a word, even when the word is not present.

    - WordFrequencyAnalyzer.calculate_most_frequent_n_words should
      always return the n most common words sorted by frequency first
      and alphabetic order second.

    The `hypothesis` package tries to intelligently test the invariants
    by generating different scenarios that include boundary conditions
    and other potentially problematic inputs.
    """

    @given(text())
    def test_word_frequencies_accepts_valid_utf8(self, sample_text: str):
        """word_frequencies should return Counter for valid utf-8 text."""
        analyzer = WordFrequencyAnalyzer(sample_text)
        self.assertIsInstance(analyzer.word_frequencies, collections.Counter)

    @given(generate_words_with_random_separators())
    def test_word_frequencies_returns_correct_counts(self, sample: tuple[str, dict[str, int]]):
        """word_frequency should return the correct word counts."""
        sample_text, word_counts = sample
        analyzer = WordFrequencyAnalyzer(sample_text)
        self.assertDictEqual(word_counts, analyzer.word_frequencies)

    @given(generate_text_known_most_common_word_frequency())
    def test_most_common_word_frequency(self, sample: tuple[str, int]):
        """word_frequency should return the most common word frequency."""
        sample_text, frequency_most_common = sample
        analyzer = WordFrequencyAnalyzer(sample_text)
        self.assertEqual(frequency_most_common, analyzer.calculate_highest_frequency())

    @given(generate_words_with_random_frequencies())
    def test_frequency_for_specific_word(self, sample: tuple[str, dict[str, int]]):
        """calculate_frequency_for_word should return the actual count."""
        sample_text, word_counts = sample
        target_word, frequency = word_counts.popitem() if word_counts else ("word", 0)
        analyzer = WordFrequencyAnalyzer(sample_text)
        self.assertEqual(frequency, analyzer.calculate_frequency_for_word(target_word))

    @given(generate_words_with_random_frequencies(), integers(min_value=0, max_value=50))
    def test_n_most_common_words(self, sample: tuple[str, dict[str, int]], n: int):
        """calculate_most_frequent_n_words should return correctly sorted most frequent words."""
        sample_text, word_counts = sample
        most_common = [
            WordFrequency(word.lower(), frequency)
            for word, frequency in sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
            if frequency > 0
        ][:n]

        analyzer = WordFrequencyAnalyzer(sample_text)
        self.assertEqual(most_common, analyzer.calculate_most_frequent_n_words(n))
