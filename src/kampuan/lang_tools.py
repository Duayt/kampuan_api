# %%
from kampuan.const import df_vowel_form, THAI_TONE
from typing import List, NamedTuple
from collections import namedtuple
import re

# %%
# Tones


def remove_tone_mark(text, tone_marks=THAI_TONE):
    for mark in tone_marks:
        text = text.replace(mark, '')
    return text

# %%

# Vowel extraction


def get_vowel_form(REP: str = '[REP]', is_sort=True) -> List[str]:
    """ Get all of Thai's vowel forms

    Args:
        REP (str, optional): string token as a placeholder for Thai vowel eg "[REP]า" ,"เ[REP]ีย". Defaults to '[REP]'.
        is_sort (bool, optional): sort the list by lenght of vowel character (longer first). Defaults to True.

    Returns:
        List[str]: List of Thai vowel forms
    """
    vowel_list = df_vowel_form['รูปสระ'].str.replace(
        '\xa0', '').str.replace('-', REP).str.strip().tolist()
    vowel_list.append(REP)
    if is_sort:
        vowel_list.sort(key=len, reverse=True)
    return vowel_list


def get_vowel_pattern(REP='[REP]') -> List[str]:
    """Get regex pattern to identify which vowel pattern is in the subword

    Args:
        REP (str, optional): string token as a placeholder for Thai vowel eg "[REP]า" ,"เ[REP]ีย". Defaults to '[REP]'.

    Returns:
        List[str]: List of regex pattern for vowel extractions
    """
    vowel_pattern = []
    vowel_forms = get_vowel_form(REP=REP)
    for vow in vowel_forms:
        if vow.startswith(REP) & vow.endswith(REP):  # case ตบ
            vowel_pattern.append(f"{vow.replace(REP,'(.{1,2})')}([ก-ฮ])")
        else:  # general case
            vowel_pattern.append(
                f"({vow.replace(REP,')(.{1,2})(')})([ก-ฮ]?)".replace('()', ''))
    return vowel_pattern


def extract_vowel_form(text:str, vowel_patterns:List[str]=None, vowel_forms:List[str]=None)-> NamedTuple:
    """Extract vowel of the subword

    Args:
        text (str):text (only single substring with single vowel)
        vowel_patterns (List[str], optional): vowel patterns for regex match. Defaults to None.
        vowel_forms (List[str], optional): vowel forms with matching order to return visually. Defaults to None.

    Returns:
        NamedTuple: namedtuple(
        'vowel_extract', ['vowel_form', 'regex', 'matched_pattern'])
    """
    vowel_extract = namedtuple(
        'vowel_extract', ['vowel_form', 'regex', 'matched_pattern'])
    if not vowel_patterns:
        vowel_patterns = get_vowel_pattern()
    if not vowel_forms:
        vowel_forms = get_vowel_form(REP='-')
    text = remove_tone_mark(text)
    for i, pattern in enumerate(vowel_patterns):
        m = re.match(pattern, text)
        if m:
            return vowel_extract(vowel_forms[i], m, pattern)

    return vowel_extract(None, text, text)


extract_vowel_form('ไก่').vowel_form
# %%


# %%
