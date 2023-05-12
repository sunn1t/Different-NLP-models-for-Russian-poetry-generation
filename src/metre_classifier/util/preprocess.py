# Borrowed from: rupo
# Source: https://github.com/IlyaGusev/rupo

import re

CYRRILIC_LOWER_VOWELS = "аоэиуыеёюя"
CYRRILIC_LOWER_CONSONANTS = "йцкнгшщзхъфвпрлджчсмтьб"
VOWELS = "aeiouAEIOUаоэиуыеёюяАОЭИУЫЕЁЮЯ"
CLOSED_SYLLABLE_CHARS = "рлймнРЛЙМН"

def count_vowels(string):
    num_vowels = 0
    for char in string:
        if char in VOWELS:
            num_vowels += 1
    return num_vowels


def get_first_vowel_position(string):
    for i, ch in enumerate(string):
        if ch in VOWELS:
            return i
    return -1
