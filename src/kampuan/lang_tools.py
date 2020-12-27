# %%
import re
from collections import namedtuple
from typing import List, NamedTuple

from kampuan.const import MUTE_MARK, THAI_CONS, THAI_TONE, VOWEL_FORMS

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
    vowel_list = [ch.replace('-', REP).strip() for ch in VOWEL_FORMS]
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
                f"({vow.replace(REP,')(.{1,3})(')})([ก-ฮ]*)".replace('()', ''))
    return vowel_pattern


def extract_vowel_form(text: str, vowel_patterns: List[str] = None, vowel_forms: List[str] = None) -> NamedTuple:
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
    # Todo remove ตัวการันต์
    text = remove_tone_mark(text)
    for i, pattern in enumerate(vowel_patterns):
        m = re.match(pattern, text)
        if m:
            return vowel_extract(vowel_forms[i], m, pattern)

    return vowel_extract(None, text, text)


def find_main_mute_consonant(text:str):
    """extract main mute consonant การันต์

    Args:
        text (str): word to check

    Returns:
        List of tuple List[(int,str)]: return[] if no การันต์ , return [(index, consonant)]
    """
    
    if MUTE_MARK not in text:
        return []
    else:
        all_con=[]
        mark_index=text.index(MUTE_MARK)
        for i in range(len(text[:mark_index])-1,0-1,-1):
            if text[i] in THAI_CONS:
                main_con = (i,text[i])
                break
        all_con.append(main_con)
        if len(all_con) >0:
            if main_con[1] == 'ร':
                lead_con_index=main_con[0]-1
                if text[lead_con_index] in ['ท','ต','ด']: #ทร์ ,ตร์ ,ดร์ 
                    all_con.append((lead_con_index,text[lead_con_index]))
            return all_con
        else:
            return []

# extract_vowel_form('ไก่').vowel_form
# %%


# %%
