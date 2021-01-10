# %%
import re
from collections import namedtuple
from typing import List, NamedTuple
import numpy as np
from pythainlp.util import normalize, num_to_thaiword
from kampuan.const import (ASPIRATE, ASPIRATE_HIGH_SOUND,
                           ASPIRATE_HIGH_SOUND_INV, ASPIRATE_LOW_SOUND,
                           ASPIRATE_LOW_SOUND_INV, FALSE_CONSONANT_CLUSTER,
                           LEADING_CONSONANT_CLUSTER, MUTE_MARK, SORONANT,
                           SOUND_CLASS, THAI_CONS, THAI_TONE, THAI_VOW,
                           TRUE_CONSONANT_CLUSTER, VOWEL_FORMS, df_tone_rule)

# %%
# Tones


def check_if_list(text):
    return (text[0] == '[' and text[-1] == ']') or (',' in text)


def handle_white_spaces(text):
    text = re.sub(' +', ',', text)
    return text


def normalize_word(text):
    return normalize(text)


def process_num_to_thaiword(texts):
    result = []
    for i, word in enumerate(texts):
        if word.isnumeric():
            result.append(num_to_thaiword(word))
        else:
            result.append(word)
    return result


def process_555(texts: List[str]):
    result = []
    for i, word in enumerate(texts):
        if word.isnumeric() and '55' in word:
            result.append(word.replace('5', 'ฮ่า'))
        else:
            result.append(word)
    return result


test_case = ['555', 'หิวข้าว55', 'กิน5มื้อ', 'กิน5ข้าว5', '5555ตลก']

# for text in test_case:
#     print(process_555(text))


def process_text_2_list(text):
    text = text.strip()
    text = handle_white_spaces(text)
    if check_if_list(text):
        # convert string to properlist
        if not (text[0] == '[' and text[-1] == ']'):
            text = '[' + text + ']'
        if '"' not in text and "'" not in text:
            text = text.replace(',', '","').replace(
                '[', '["').replace(']', '"]')

        text = eval(text)  # can input list
    return text


def insert_ch_after(text, ch, index):
    return text[:index+1] + ch + text[index+1:]


def remove_tone_mark(text, tone_marks=THAI_TONE):
    for mark in tone_marks:
        text = text.replace(mark, '')
    return text


# %%
test = ['ได้', 'ๆ', 'ไป', 'กิน', 'บ่อย', 'ๆ', 'ๆ']
test_result = ['ได้', 'ได้', 'ไป', 'กิน', 'บ่อย', 'บ่อย', 'บ่อย']


def process_double(texts):
    result = []
    for i, word in enumerate(texts):
        if word == 'ๆ' and i > 0:
            result.append(result[i-1])
        else:
            result.append(word)
    return result


assert process_double(test) == test_result


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
        vowel_list.sort(reverse=True)
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


def extract_vowel_form(text: str,
                       vowel_patterns: List[str] = None,
                       vowel_forms: List[str] = None) -> NamedTuple:
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


def find_main_mute_consonant(text: str):
    """extract main mute consonant การันต์

    Args:
        text (str): word to check

    Returns:
        List of tuple List[(int,str)]: return[] if no การันต์ , return [(index, consonant)]
    """

    if MUTE_MARK not in text:
        return []
    else:
        all_con = []
        mark_index = text.index(MUTE_MARK)
        for i in range(len(text[:mark_index])-1, 0-1, -1):
            if text[i] in THAI_CONS:
                main_con = (i, text[i])
                break
        all_con.append(main_con)
        if len(all_con) > 0:
            if main_con[1] == 'ร':
                lead_con_index = main_con[0]-1
                if text[lead_con_index] in ['ท', 'ต', 'ด']:  # ทร์ ,ตร์ ,ดร์
                    all_con.append((lead_con_index, text[lead_con_index]))
            return all_con
        else:
            return []


def find_mute_vowel(text: str):
    """extract main mute vowel การันต์ case:('พันธุ์')

    Args:
        text (str): word to check

    Returns:
        List of tuple List[(int,str)]: return[] if no การันต์ , return [(index, consonant)]
    """

    if MUTE_MARK not in text:
        return []
    else:
        mark_index = text.index(MUTE_MARK)
        lead_mute = text[mark_index-1]
        if lead_mute in THAI_VOW:
            return [(mark_index-1, lead_mute)]
        else:
            return []


def get_tone_sound_row(tone_group_rule, word_class, vowel_class):
    filters = (df_tone_rule['tone_group_rules'] == tone_group_rule) &\
        (df_tone_rule['word_class'] == word_class) &\
        (df_tone_rule['vowel_class'] == vowel_class)
    return df_tone_rule[filters].iloc[0, 3:]


def determine_tone_sound(tone_mark_class, tone_group_rule, word_class, vowel_class):
    df_row = get_tone_sound_row(tone_group_rule, word_class, vowel_class)
    return np.where(df_row == tone_mark_class)[0].item()


def convert_tone_pair_single_init(ch: str):
    assert len(ch) == 1
    if ch in SORONANT:
        if ch == 'ฬ':
            return 'หล'
        elif ch == 'ณ':
            return 'หน'
        else:
            return 'ห'+ch  # neglect   'อ' นำ case
    elif SOUND_CLASS[ch] == 'mid':
        return ch
    elif ch in ASPIRATE:
        if ch in ASPIRATE_LOW_SOUND.keys():
            en = ASPIRATE_LOW_SOUND[ch]
            return ASPIRATE_HIGH_SOUND_INV[en]
        else:
            en = ASPIRATE_HIGH_SOUND[ch]
            return ASPIRATE_LOW_SOUND_INV[en]


def convert_tone_pair_double_init(ch: str, tractor_case=False):  # แทร็กเตอร์
    assert len(ch) > 1
    if ch in LEADING_CONSONANT_CLUSTER:
        return ch[-1]
    elif ch == 'ทร':
        if tractor_case:
            return 'ถร'
        else:
            return 'ส'
    elif ch in TRUE_CONSONANT_CLUSTER+FALSE_CONSONANT_CLUSTER:
        init = convert_tone_pair_single_init(ch[0])
        final = ch[1]
        return init+final
    else:
        raise ValueError(f'Not implement {ch}')

        # %%
# to move to test
if False:
    for ch in THAI_CONS:
        new_ch = convert_tone_pair_single_init(ch)
        if len(new_ch) > 1:
            print(ch, new_ch, convert_tone_pair_double_init(new_ch))
        else:
            print(ch, new_ch)

    for ch in TRUE_CONSONANT_CLUSTER:
        print(ch, convert_tone_pair_double_init(ch))
        # %%
