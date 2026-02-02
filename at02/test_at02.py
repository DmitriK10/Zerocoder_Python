import pytest
from main_at02 import count_vowels

def test_all_vowels():
    assert count_vowels("aeiouAEIOU") == 10

def test_empty_string():
    assert count_vowels("") == 0

def test_only_consonants():
    assert count_vowels("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ") == 0

def test_mixed_vowels():
    assert count_vowels("Hello Python World") == 4

def test_with_numbers():
    assert count_vowels("a1e2i3o4u5") == 5

def test_with_special_chars():
    assert count_vowels("a!e@i#o$u%") == 5

@pytest.mark.parametrize("input_text, expected", [
    ("Test", 1),
    ("PROGRAMMING", 3),
    ("qwerty", 1),
    ("AEI OU", 5),
    ("bcd", 0),
    ("A", 1),
    ("z", 0),
])
def test_various_inputs(input_text, expected):
    assert count_vowels(input_text) == expected