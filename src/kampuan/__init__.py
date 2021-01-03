from typing import List, Union, Dict
import pythainlp.tokenize as tk
from pythainlp.tokenize import syllable_tokenize
from kampuan.lang_tools import extract_vowel_form
from kampuan.sub_word import ThaiSubWord

# Lu2Thai related libraries
import json
from kampuan.const import LU_SYLLABLE_FILENAME
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import Trie as dict_trie
from pythainlp.corpus.common import thai_syllables

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..., ref https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list"
    a = iter(iterable)
    return zip(a, a)

def test(name: str = "World!"):
    return f'Hello {name}'


def tokenize(text: str = "สวัสดี") -> List[str]:
    # return tk.word_tokenize(text=phrase)
    return syllable_tokenize(text=text)


def extract_vowel(text: str) -> Dict:
    if isinstance(text, str):
        phrases = tokenize(text=text)
    results = {}
    for word in text:
        results[word] = extract_vowel_form(word).vowel_form

    return results

def syllable_tokenize_lu(text: str) -> List[str]:    
    """Reference https://thainlp.org/pythainlp/docs/2.0/_modules/pythainlp/tokenize.html#syllable_tokenize"""
    if not text or not isinstance(text, str):
        return []

    tokens = []
    # Read lu syllable list
    with open(LU_SYLLABLE_FILENAME, 'r') as f:
        syllable_lu_dict = json.load(f) 
    
    # Create custom dict trie for Lu
    lu_syllable = syllable_lu_dict['data']
    dict_source = frozenset(set(lu_syllable))
    trie = dict_trie(dict_source)

    if text:        
        words = word_tokenize(text, custom_dict=trie)
        #print("lu", words)
        #dict_source = frozenset(set(lu_syllable).union(set(thai_syllables())))        
        for word in words:
            tokens.extend(word_tokenize(text=word, custom_dict=trie))

    return tokens

def puan_kam_preprocess(text, skip_tokenize=True, flag_lu_2_thai=False):
    # 2. Split phrase to syllables
    if isinstance(text, str):
        tokenized = tokenize(text)
        if flag_lu_2_thai: tokenized = syllable_tokenize_lu(text)
    elif isinstance(text, List):
        if skip_tokenize:
            tokenized = text
        else:
            if not flag_lu_2_thai: tokenized = [w for txt in text for w in tokenize(txt)]
            else: tokenized = [w for txt in text for w in syllable_tokenize_lu(txt)]
    else:
        raise ValueError('incorrect value')
    # 3. Sub word processing, types and tones
    sub_words = [ThaiSubWord(word, lu_word=flag_lu_2_thai) for word in tokenized]

    # 4. preprocessing on two syllable words
    # Lu2Thai remark : should not need to check non_conform word
    if not flag_lu_2_thai:
        split_words = [
            word_split for word in sub_words for word_split in word.split_non_conform()]
    else: split_words = sub_words

    return split_words

def lu_2_thai(text):
    """ module that converts Lu words to somewhat readable Thai words
        Lu module does not need index so should be able to wrap everything in one module cleanly
    """
    
    if isinstance(text, str):
        subwords = puan_kam_preprocess(text, flag_lu_2_thai=True)
    elif isinstance(text[0], str):
        subwords = puan_kam_preprocess(text, flag_lu_2_thai=True)
    else:
        subwords = text

    output_thai = []    
    # Iterate every 2 syllable 
    for a_first, a_second in pairwise(subwords):    
        # Check special case รอ ลอ สอ ซอ
        if a_first.init_con not in ['ซ', 'ส']:
            thai_out = a_first._vowel_form_sound.replace('-', a_second.init_con) + a_first.final_con            
        else:
            thai_out = a_first._vowel_form_sound.replace('-', 'ล') + a_first.final_con
        # No need to check case อุ อู
                
        thai_out = ThaiSubWord(thai_out)
        
        # Assign tone of second lu words to that_out, this tone should be the same with original Thai word
        thai_out = ThaiSubWord.pun_wunayook(thai_out.raw, a_first._tone)
        output_thai.append(thai_out)            

    return output_thai

def puan_2_lu(subwords, lu_tuple=False):
    """ Leverage existing puan kum method to convert to lu language"""
    output_lu = []
    
    for subword in subwords:        
        a_raw = subword
        # get vowel and change init consonant to ล, also keep oritinal form and sound for first
        # Check special case รอ ลอ สอ ซอ
        if a_raw.init_con not in ['ล', 'ร', 'ฤ', 'หล', 'หร']:
            if len(a_raw.tone_mark) > 0: a_first = a_raw._vowel_form_sound.replace('-', 'ล') + a_raw.final_con    
            else: a_first = a_raw._vowel_form_sound.replace('-', 'ล') + a_raw.final_con
        else:
            if len(a_raw.tone_mark) > 0: a_first = a_raw._vowel_form_sound.replace('-', 'ซ') + a_raw.final_con    
            else: a_first = a_raw._vowel_form_sound.replace('-', 'ซ') + a_raw.final_con
        
        # Check special case อุ อู
        if a_raw._vowel_form_sound.replace('-', '') == "ู": a_second = a_raw.main_init_sound + "ี" + a_raw.final_con
        elif a_raw._vowel_form_sound.replace('-', '') == "ุ": a_second = a_raw.main_init_sound + "ิ" + a_raw.final_con            
        else:
            if a_raw._vowel_class == 'short': a_second = a_raw.main_init_sound + "ุ" + a_raw.final_con
            else: a_second = a_raw.main_init_sound + "ู" + a_raw.final_con
            
        a_first = ThaiSubWord(a_first)
        a_second = ThaiSubWord(a_second)    
        
        # Assign tone of original word to both first and second lu
        a_first = ThaiSubWord.pun_wunayook(a_first.raw, a_raw._tone)    
        a_second = ThaiSubWord.pun_wunayook(a_second.raw, a_raw._tone)
        
        # Default to return as list of all lu syllables
        if not lu_tuple:
            output_lu.append(a_first)
            output_lu.append(a_second)
        else:
        # Return as tuple of lu rather than concat together        
            output_lu.append((a_first, a_second))
        #output_lu.append(a_target)        
            
    return output_lu

def puan_2_kam(a_raw, b_raw, keep_tone=None):
    a_raw_tone = a_raw._tone
    b_raw_tone = b_raw._tone

    # swap vowel
    a_target = b_raw._vowel_form_sound.replace('-', a_raw.init_con)
    b_target = a_raw._vowel_form_sound.replace('-', b_raw.init_con)

    # swap final con
    a_target = ThaiSubWord(a_target + b_raw.final_con)
    b_target = ThaiSubWord(b_target + a_raw.final_con)

    # Swap tone
    # assign tones
    if keep_tone is None:
        if a_target._word_class == 'dead' or b_target._word_class == 'dead':
            keep_tone = False
        else:
            keep_tone = True

    if keep_tone:
        a_target_tone = a_raw_tone
        b_target_tone = b_raw_tone
    else:
        a_target_tone = b_raw_tone
        b_target_tone = a_raw_tone

    # apply tone rules
    a_target = ThaiSubWord.pun_wunayook(a_target._raw, a_target_tone)
    b_target = ThaiSubWord.pun_wunayook(b_target._raw, b_target_tone)

    return a_target, b_target


def puan_kam_base(text='สวัสดี', keep_tone=None, use_first=True, index=None, flag_puan_2_lu=False, lu_tuple=False):

    if isinstance(text, str):
        split_words = puan_kam_preprocess(text)
    elif isinstance(text[0], str):
        split_words = puan_kam_preprocess(text)
    else:
        split_words = text
    # 5. Determine two syllable to do the puan
    if not index:
        n_subwords = len(split_words)
        index = (0, 0)
        if n_subwords == 1:
            index = (0, 0)
        elif n_subwords == 2:
            index = (0, 1)
        elif use_first:
            index = (0, -1)
        else:
            index = (1, -1)
    # 6. Puan process, output new
    # puan kum given two subwords
    a_raw = split_words[index[0]]
    b_raw = split_words[index[1]]

    # apply tone rules
    if not flag_puan_2_lu: a_target, b_target = puan_2_kam(a_raw, b_raw)
    else: return puan_2_lu(split_words, lu_tuple=lu_tuple)

    # 7. combine
    kam_puan = [w._raw for w in split_words]
    kam_puan[index[0]] = a_target
    kam_puan[index[1]] = b_target

    return kam_puan


def puan_kam_all(text='สวัสดี'):
    use_first = [True, False]
    keep_tone = [True, False]
    result = {}
    count = 0
    for j in use_first:
        for k in keep_tone:
            result[count] = puan_kam_base(
                text=text, use_first=j, keep_tone=k)
            count += 1
    return result

def puan_kam_lu(text, lu_tuple=False):
    """Seperate module for lu for greater simplicity"""
    if isinstance(text, str):
        split_words = puan_kam_preprocess(text)
    elif isinstance(text[0], str):
        split_words = puan_kam_preprocess(text)
    else:
        split_words = text

    n_subwords = len(split_words)
    
    # Flag to return without having to find index
    return puan_kam_base(text=split_words, keep_tone=None, lu_tuple=lu_tuple, flag_puan_2_lu=True)

def puan_kam_auto(text='สวัสดี', use_first=None):

    if isinstance(text, str):
        split_words = puan_kam_preprocess(text)
    elif isinstance(text[0], str):
        split_words = puan_kam_preprocess(text)
    else:
        split_words = text

    n_subwords = len(split_words)

    index = (0, 0)
    if n_subwords == 1:
        index = (0, 0)
    elif n_subwords == 2:
        index = (0, 1)
    elif n_subwords == 3:
        if split_words[0]._word_class == 'dead':  # not sure
            index = (1, -1)
        else:
            index = (0, -1)
    else:  # more than 3        
        if use_first is None:
            return [puan_kam_base(text=split_words, keep_tone=None, index=(i, -1)) for i in [0, 1]]
        elif use_first:
            index = (0, -1)
        else:
            index = (1, -1)

    return puan_kam_base(text=split_words, keep_tone=None, index=index)


def puan_kam(text) -> List[str]:
    return puan_kam_auto(text=text, use_first=None)

def puan_lu(text, lu_tuple=False) -> List[str]:
    return puan_kam_lu(text=text, lu_tuple=lu_tuple)

def translate_lu(text) -> List[str]:
    return lu_2_thai(text=text)

def pun_wunayook(text):
    text = puan_kam_preprocess(text)
    result = []
    for i, txt in enumerate(text):
        result.append([ThaiSubWord.pun_wunayook(txt._raw, tone_target=i)
                       for i in range(0, 5)])
    return result
