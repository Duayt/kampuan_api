# %%
from kampuan.lang_tools import extract_vowel_form,get_vowel_form
import pytest

def test_vowel_form():
    """ test vowel form"""

    vowel_forms = get_vowel_form()
    assert len(vowel_forms) == 38


def test_extract_cases(words):

    assert extract_vowel_form(words.raw).vowel_form == words.vowel_form