# Read Asset
import pythainlp
import pandas as pd

df_init_con =pd.read_excel('../src/kampuan/assets/initial_consonants.xlsx',skiprows=1).fillna(method='ffill')
df_fin_con =pd.read_excel('../src/kampuan/assets/final_consonants.xlsx',skiprows=1)
df_fin_con['sound']=df_fin_con['sound'].fillna(method='ffill')
df_vowel_form =pd.read_excel('../src/kampuan/assets/thai_vowel_forms.xlsx')

THAI_CHARS =pythainlp.thai_characters
THAI_CONS =pythainlp.thai_consonants
THAI_VOW =pythainlp.thai_vowels
THAI_TONE=pythainlp.thai_tonemarks