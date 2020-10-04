# %%
from kampuan.lang_tools import extract_vowel_form,get_vowel_form
import pytest

def test_vowel_form():
    """ test vowel form"""

    vowel_forms = get_vowel_form()
    assert len(vowel_forms) == 38


def test_extract_cases(test_words):

    assert extract_vowel_form(test_words.raw).vowel_form == test_words.vowel_form