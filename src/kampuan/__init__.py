from typing import List, Union, Dict
import pythainlp.tokenize as tk
from pythainlp.tokenize import syllable_tokenize
from kampuan.lang_tools import extract_vowel_form


def test(name: str = "World!"):
    return f'Hello {name}'


def tokenize(phrase: str = "สวัสดี") -> List[str]:
    # return tk.word_tokenize(text=phrase)
    return syllable_tokenize(text=phrase)


def puan_kam(phrase: Union[List[str], str] = ['กิน', 'ข้าว']) -> List[str]:

    if isinstance(phrase, str):
        phrase = tokenize(phrase=phrase)

    return phrase


def extract_vowel(phrases: str) -> Dict:
    if isinstance(phrases, str):
        phrases = tokenize(phrase=phrases)
    results = {}
    for word in phrases:
        results[word] = extract_vowel_form(word).vowel_form

    return results
