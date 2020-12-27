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

THAI_CHARS = pythainlp.thai_characters
THAI_CONS = pythainlp.thai_consonants
THAI_VOW = pythainlp.thai_vowels
THAI_TONE = pythainlp.thai_tonemarks
REP = '[REP]'
