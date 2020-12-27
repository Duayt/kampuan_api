# Read Asset
import pythainlp
import pandas as pd
import os
dirname = os.path.dirname(__file__)

df_init_con = pd.read_excel(os.path.join(dirname,
                                         'assets/initial_consonants.xlsx'), skiprows=1, engine='openpyxl').fillna(method='ffill')
df_fin_con = pd.read_excel(os.path.join(dirname,
                                        'assets/final_consonants.xlsx'), skiprows=1, engine='openpyxl')
df_fin_con['sound'] = df_fin_con['sound'].fillna(method='ffill')
df_vowel_form = pd.read_excel(os.path.join(dirname,
                                           'assets/thai_vowel_forms.xlsx'), engine='openpyxl')

VOWEL_FORMS_W_CONSONANT = [
    '-ือ',
    'เ-ียะ',
    'เ-ีย',
    'เ-ือะ',
    'เ-ือ',
    '-ัวะ',
    '-ัว',
    '-ว',
    '-็อ',
    '-อ',
    'เ-อะ',
    'เ-อ',
]  # assume last cons is vowel

VOWEL_FORMS_W_LEADING = [
    'ใ-',
    'ไ-',
    # 'ใ-ย',
    'เ-',
    'แ-',
    'โ-',
]  # special rules on cluster

VOWEL_FORM_BASIC = [
    '-ะ',
    '-ั',
    '-ำ',
    'เ-า',
    '-า',
    '-ิ',
    '-ี',
    '-ึ',
    '-ื',
    '-ุ',
    '-ู',
    'เ-ะ',
    'เ-็',
    'แ-ะ',
    'แ-็',
    'โ-ะ',
    'เ-าะ',
    '-็',
    'เ-ิ',
]
VOWEL_FORMS = VOWEL_FORM_BASIC + VOWEL_FORMS_W_CONSONANT + VOWEL_FORMS_W_LEADING
THAI_CHARS = pythainlp.thai_characters
THAI_CONS = pythainlp.thai_consonants
THAI_VOW = pythainlp.thai_vowels
THAI_TONE = pythainlp.thai_tonemarks
TRUE_CONSONANT_CLUSTER = [
    'กร',
    'กล',
    'กว',
    'ขร',
    'ขล',
    'ขว',
    'คร',
    'คล',
    'คว',
    'ตร',
    'ปร',
    'ปล',
    'ผล',
    'พร',
    'พล',
    'บร',
    'บล',
    'ดร',
    'ฟร',
    'ฟล',
    'ทร',  # แทร็กเตอร์ ทรัมเป็ต ทรัส (with upper vowel???)
]

FALSE_CONSONANT_CLUSTER = [
    'ทร',
    'สร',
    'ซร',
    'จร',
]
LEADING_CONSONANT_CLUSTER = [
    'หง',
    'หน',
    'หม',
    'หย',
    'หร',
    'หล',
    'หว',
    'อย'
]
NON_CONFORMING_CONSONANT_CLUSTER=[
    
]
ALL_CONSONANT_CLUSTER = list(
    set(TRUE_CONSONANT_CLUSTER + FALSE_CONSONANT_CLUSTER+LEADING_CONSONANT_CLUSTER))

DOUBLE_FINAL_CONSONANT = [
    'ตร',
    'ชร',
    'ทร',
    'รถ',
    'รท',
]

MUTE_MARK = '\u0e4c'
REP = '[REP]'
