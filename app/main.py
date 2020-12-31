import kampuan as kp
import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
app = FastAPI(title="Kampuan project",
              description="Welcome, This is a project using python to do คำผวน by Tanawat C. \n https://www.linkedin.com/in/tanawat-chiewhawan",
              version="0.0.1",)


@app.get("/", include_in_schema=False)
async def root():
    # return {'message': "Hello welcome to Kampuan API (คำผวน)",
    #         'author': "Tanawat C."}
    response = RedirectResponse(url='/docs')
    return response


def check_if_list(text):
    return (text[0] == '[' and text[-1] == ']') or (',' in text)


def process_text_2_list(text):
    text = text.strip()

    if check_if_list(text):
        # convert string to properlist
        if not (text[0] == '[' and text[-1] == ']'):
            text = '[' + text + ']'
        if '"' not in text and "'" not in text:
            text = text.replace(',', '","').replace(
                '[', '["').replace(']', '"]')

        text = eval(text)  # can input list
    return text


@app.get("/puan_kam/{text}")
def puan_kam(text: str = 'สวัสดี',
             first: Optional[bool] = None,
             keep_tone: Optional[bool] = None,
             all: Optional[bool] = False,
             skip_tokenize: Optional[bool] = None):
    """Puan kum (ผวนคำ) is a Thai toung twister, is API convert string into kampuan
        Play around with the options to see different results.

    -Args:
    - **text** (str):  Defaults to 'สวัสดี'.
        - input string 'ไปเที่ยว' -> auto tokenize will apply and split to ไป and  เที่ยว
        - list of string which accepted 3 formats: ['ไป','กิน','ข้าว'] | 'ไป','กิน','ข้าว' | ไป,กิน,ข้าว, the list input will also neglect auto tokenization.
    - **first** (bool, optional): if True use the first word  to puan together with the last word otherwise will select second word and last word
                                    (None will let us decide). Defaults to None.

    - **keep_tone** (bool, optional): force whether to keep the tone when doing the puan (None will let us decide). Defaults to None.

    - **all** (bool, optional): if True will provide all 4 puan results. Defaults to False.

    - **skip_tokenize** (bool, optional): if True will skip tokenzation and use user provided list of words (input pure string will force to False or dont skip tokenization). Defaults to None.

    -Returns:
    - **results**: List of คำผวน
    """
    if not check_thai_ch(text):
        return HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)

    try:
        split_words = kp.puan_kam_preprocess(text, skip_tokenize=skip_tokenize)
    except ValueError as e:
        try:
            split_words = kp.puan_kam_preprocess(text, skip_tokenize=True)
        except ValueError as e:
            return HTTPException(422, detail=f'Input error: {e}')

    if all is not None and all:
        return {'input': text,
                'results': kp.puan_kam_all(text=split_words)}
    else:
        if first is None and keep_tone is None:
            return {'input': text,
                    'results': kp.puan_kam(text=split_words)}
        else:
            return {'input': text,
                    'results': kp.puan_kam_base(text=split_words, keep_tone=keep_tone, use_first=first)}


@app.get("/puan_lu/{text}")
def puan_lu(text: str = 'สวัสดี',
            skip_tokenize: Optional[bool] = None):
    """ภาษาลู

    -Args:
    - **text** (str):  Defaults to 'สวัสดี'.
        - input string 'ไปเที่ยว' -> auto tokenize will apply and split to ไป and  เที่ยว
        - list of string which accepted 3 formats: ['ไป','กิน','ข้าว'] | 'ไป','กิน','ข้าว' | ไป,กิน,ข้าว, the list input will also neglect auto tokenization.

    -Returns:
    - **results**: List of คำผันลู
    """
    if not check_thai_ch(text):
        return HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)
    try:
        split_words = kp.puan_kam_preprocess(text, skip_tokenize=skip_tokenize)
    except ValueError as e:
        try:
            split_words = kp.puan_kam_preprocess(text, skip_tokenize=True)
        except ValueError as e:
            return HTTPException(422, detail=f'Input error: {e}')

    return {'input': text,
            'results': kp.puan_lu(text=split_words)}


@app.get("/pun_wunnayook/{text}")
def pun_wunnayook(text: str = 'สวัสดี'):
    """pun wunnayook (ผันเสียงวรรณยุกต์)

    -Args:
    - **text** (str):  Defaults to 'สวัสดี'.
        - input string 'ไปเที่ยว' -> auto tokenize will apply and split to ไป and  เที่ยว
        - list of string which accepted 3 formats: ['ไป','กิน','ข้าว'] | 'ไป','กิน','ข้าว' | ไป,กิน,ข้าว, the list input will also neglect auto tokenization.

    -Returns:
    - **results**: List of คำผัน
    """
    if not check_thai_ch(text):
        return HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)
    return kp.pun_wunayook(text=text)


@app.get("/vowel/{text}")
def extract_vowel(text: str = 'สวัสดี'):
    """ Method to extract Thai vowel form out.

    -Args:

    - **text** (str):  Defaults to 'สวัสดี'.
        - input string 'ไปเที่ยว' -> auto tokenize will apply and split to ไป and  เที่ยว
        - list of string which accepted 3 formats: ['ไป','กิน','ข้าว'] | 'ไป','กิน','ข้าว' | ไป,กิน,ข้าว, the list input will also neglect auto tokenization.

    -Returns:
    - **results**: List of extracted vowel
    """
    if not check_thai_ch(text):
        return HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)
    if isinstance(text, str):
        text = kp.tokenize(text)
    return {"input": text,
            "result": kp.extract_vowel(text)}


@app.get("/is_thai/{text}")
def check_thai_ch(text):
    return all(w in kp.const.ACCEPT_CHARS for w in text)
