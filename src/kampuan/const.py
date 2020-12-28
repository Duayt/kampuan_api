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
MUTE_MARK = '\u0e4c'
REP = '[REP]'

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
SHORT_SOUND_VOWELS = [
    '-ะ',
    '-ิ',
    '-ึ',
    '-ุ',
    'เ-ะ',
    'แ-ะ',
    'เ-็',
    'แ-็',
    'โ-ะ',
    'เ-าะ',
    'เ-อะ',
    'เ-ียะ',
    'เ-ือะ',
    '-ัวะ',
    'ฤ',
    'ฦ',
    '-ำ',
    'ไ-',
    'ใ-',
    'เ-า',
]
LONG_SOUND_VOWELS = [vw for vw in VOWEL_FORMS if vw not in SHORT_SOUND_VOWELS]
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
NON_CONFORMING_CONSONANT_CLUSTER = [

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
# for sound tone
SORONANT_SOUND = {
    'ง': 'ng',
    'ณ': 'n', 'น': 'n',
    'ม': 'm',
    'ญ': 'y', 'ย': 'y',
    'ร': 'r',
    'ฬ': 'l', 'ล': 'l',
    'ว': 'w',
}

SORONANT = list(SORONANT_SOUND.keys())

PLAIN_SOUND = {
    'ก': 'g',
    'จ': 'j',
    'ฎ': 'd', 'ด': 'd',
    'ฏ': 'dt', 'ต': 'dt',
    'บ': 'b',
    'ป': 'bp',
    'อ': 'o',
}

ASPIRATE_LOW_SOUND = {
    'ฅ': 'kh', 'ฆ': 'kh', 'ค': 'kh',
    'ฌ': 'ch', 'ช': 'ch',
    'ฑ': 'th', 'ฒ': 'th', 'ธ': 'th', 'ท': 'th',
    'ภ': 'ph', 'พ': 'ph',
    'ฟ': 'f',
    'ทร': 's', 'ซ': 's',
    'ฮ': 'h',

}
ASPIRATE_LOW_SOUND_INV = {v: k for k, v in
                          ASPIRATE_LOW_SOUND.items()
                          }
ASPIRATE_HIGH_SOUND = {
    'ข': 'kh', 'ฃ': 'kh',
    'ฉ': 'ch',
    'ถ': 'th', 'ฐ': 'th',
    'ผ': 'ph',
    'ฝ': 'f',
    'ส': 's', 'ศ': 's', 'ษ': 's',
    'ห': 'h',
}

ASPIRATE_HIGH_SOUND_INV = {v: k for k, v in
                           ASPIRATE_HIGH_SOUND.items()
                           }

ASPIRATE = list(ASPIRATE_LOW_SOUND.keys()) + list(ASPIRATE_HIGH_SOUND.keys())
SOUND_CLASS = {
    k: 'mid' if k in PLAIN_SOUND.keys() else 'high' if k in ASPIRATE_HIGH_SOUND.keys() else 'low' for k in THAI_CONS
}

ALL_SOUND = SORONANT_SOUND.copy()
ALL_SOUND.update(ASPIRATE_LOW_SOUND)
ALL_SOUND.update(ASPIRATE_HIGH_SOUND)
ALL_SOUND.update(PLAIN_SOUND)

TONE_MARK_CLASS = {
    "\u0e48": 1,
    "\u0e49": 2,
    "\u0e4a": 3,
    "\u0e4b": 4,
}
