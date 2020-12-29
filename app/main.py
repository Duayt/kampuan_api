import kampuan as kp
import json
from typing import Optional
from fastapi import FastAPI
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


@app.get("/puan_kam/{text}")
async def puan_kam(text: str = 'สวัสดี',
                   first: Optional[bool] = None,
                   keep_tone: Optional[bool] = None,
                   all: Optional[bool] = False):
    """Puan kum (ผวนคำ) is a Thai toung twister, is API convert string into kampuan

    -Args:
    - **text** (str): input string 'ไปเที่ยว' 
                    or list of string which accepted 3 formats ['ไป','กิน','ข้าว'] | 'ไป','กิน','ข้าว' | ไป,กิน,ข้าว. Defaults to 'สวัสดี'.
    - **first** (bool, optional): if True will use word letter to puan wiht the last other wise will select second word
                                    (None will let us decide). Defaults to None.

    - **keep_tone** (bool, optional): Force wheter to keep the tone when doing the puan (None will let us decide). Defaults to None.

    - **all** (bool, optional): if True will provide all 4 puan results. Defaults to False.

    -Returns:
    - **results**: List of คำผวน
    """
    text = text.strip()

    if check_if_list(text):
        # convert string to properlist
        if not (text[0] == '[' and text[-1] == ']'):
            text = '[' + text + ']'
        if '"' not in text and "'" not in text:
            text = text.replace(',', '","').replace(
                '[', '["').replace(']', '"]')

        text = eval(text)  # can input list
    if all:
        return {'input': text,
                'results': kp.puan_kam_all(text=text)}
    else:
        if first is None and keep_tone is None:
            return {'input': text,
                    'results': kp.puan_kam(text=text)}
        else:
            return {'input': text,
                    'results': kp.puan_kam_base(text=text, keep_tone=keep_tone, use_first=first)}


@app.get("/pun_wunnayook/{text}")
async def pun_wunnayook(text: str = 'สวัสดี'):
    """pun wunnayook (ผันเสียงวรรณยุกต์)

    -Args:
    -**text** (str): text input to do pun wunnayook Defaults to 'สวัสดี'.

    -Returns:
    - **results**: List of คำผัน
    """
    return kp.pun_wunayook(text=text)


@app.get("/vowel/{text}")
async def extract_vowel(text: str = 'สวัสดีครับ'):
    """ Method to extract Thai vowel form out.

    -Args:
    - **text** (str, optional): [description]. Defaults to 'สวัสดีครับ'.

    -Returns:
    - **results**: List of extracted vowel
    """
    text = kp.tokenize(text)
    return {"input": text,
            "result": kp.extract_vowel(text)}
