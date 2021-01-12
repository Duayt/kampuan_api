
from kampuan.lang_tools import (extract_vowel_form, get_vowel_form,
                                get_vowel_pattern)
import logging
logger = logging.getLogger(__name__)


def test_vowel_form():
    """ test vowel form"""

    vowel_forms = get_vowel_form()
    vowel_pattern = get_vowel_pattern()
    assert len(vowel_forms) == 37
    assert len(vowel_pattern) == 37


def test_extract_cases(words):
    extracted = extract_vowel_form(words.raw).vowel_form
    logger.debug(words.raw, extracted, words.vowel_form)

    assert extracted == words.vowel_form
