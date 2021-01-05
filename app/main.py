import json
import os
import re
from typing import Optional
from datetime import datetime
from datetime import datetime, timezone

import kampuan as kp
from fastapi import FastAPI, HTTPException, Request
# from starlette.requests import Request
from fastapi.responses import JSONResponse, Response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (JoinEvent, MessageEvent, TextMessage,
                            TextSendMessage)
from starlette.responses import RedirectResponse

from .firebase import FireBaseDb
from .const import ALL_CONST

# variables
<<<<<<< HEAD
ENV = 'lu'
=======
ENV = str(os.getenv('ENV', 'test'))

>>>>>>> master
CHANNEL_SECRET = str(os.getenv('CHANNEL_SECRET'))
CHANNEL_ACCESS_TOKEN = str(os.getenv('CHANNEL_ACCESS_TOKEN'))
GOOGLE_APPLICATION_CREDENTIALS = str(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

DB = str(os.getenv('FIRESTORE_DB'))
DB_ERR = str(os.getenv('FIRESTORE_DB_ERR'))
port = int(os.getenv("PORT", 5000))

if ENV == 'test':
    CONST = ALL_CONST['puan']
else:
    CONST = ALL_CONST[ENV]

# setup
app = FastAPI(title="Kampuan project",
              description="Welcome, This is a project using python to do คำผวน by Tanawat C. \n https://www.linkedin.com/in/tanawat-chiewhawan",
              version="0.0.1",)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
db = FireBaseDb(DB, credential_json=GOOGLE_APPLICATION_CREDENTIALS)
# db.test()
bot_info = line_bot_api.get_bot_info()


@ app.post("/callback", include_in_schema=False)
async def callback(request: Request):

    # get X-Line-Signature header value]
    signature = request.headers['x-line-signature']

    # get request body as text
    body = await request.body()
    body = body.decode('utf-8')
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        return HTTPException(400, detail=f'error')

    return 'OK'


def handle_message_puan(event: MessageEvent):
    text = event.message.text
    # puan process usage
    use_first = text.startswith('@')
    text = text.replace('@', '')
    puan_result = puan_kam(text=text, skip_tokenize=True, first=use_first)
    puan_result['msg'] = ''.join(puan_result['results'])
    return puan_result


def handle_message_pun(event):
    text = event.message.text
    puan_result = {}
    puan_result = pun_wunnayook(text=text)
    puan_result['msg'] = '\n'.join([' '.join(pun)
                                    for k, pun in puan_result['results'].items()])
    return puan_result


def handle_message_lu(event):
    text = event.message.text
    translate_lu = text.startswith('@')
    text = text.replace('@', '')
    puan_result = puan_lu(text=text, translate_lu=translate_lu)
    puan_result['msg'] = ''.join(puan_result['results'])
    return puan_result


handle_dict = {
    'puan': handle_message_puan,
    'pun': handle_message_pun,
    'lu': handle_message_lu
}


def process_test(text):
    list_text = text.split('$$')
    text = list_text[1]
    env_test = list_text[0]
    return text, env_test


def reply_howto():

    return CONST['how_to']


@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    event_dict = {}
    event_dict['timestamp'] = datetime.now(timezone.utc)
    event_dict['event'] = event.as_json_dict()

    if ENV == 'test':
        try:
            text, env_test = process_test(text)
            event.message.text = text
            handle_funct = handle_dict[env_test]
        except:
            handle_funct = handle_dict['puan']
    else:
        handle_funct = handle_dict[ENV]

    msg = ''
    if text == '#'+str(bot_info.display_name):  # show manual
        msg = reply_howto()
        event_dict['bot_reply'] = True

    elif text == '#hi':
        msg = bot_info.display_name
        event_dict['bot_reply'] = True

    elif text == '#ออกไปเลยชิ่วๆ':
        if event.source.type == 'user':
            msg = f'ไม่ออก! นี่มันไม่ใช่ห้องจ้า{profile.display_name}'
            event_dict['bot_reply'] = True
        else:
            msg = f'{bot_info.display_name} ลาก่อนจ้า'
            event_dict['bot_action'] = 'leave'
            event_dict['bot_reply'] = True

    else:
        try:
            # puan process usage
            puan_result = handle_funct(event)
            msg = puan_result['msg']
            event_dict['puan_result'] = puan_result
            event_dict['bot_reply'] = True
        except Exception as e:
            msg = f"""ขออภัย {bot_info.display_name} ไม่เข้าใจ {text}"""
            # f"""{profile.display_name}:{text}
            # \n ประโยคเหนือชั้นมาก! {bot_info.display_name} ยังต้องเรียนรู้อีก!
            # \n ลองใช้เฉพาะอักษรไทย หรือ เว้นวรรค ระว่าง คำ/พยางค์ ให้หน่อยจ้า
            # """
            error_msg = f'{str(repr(e))}'
            print(error_msg)
            event_dict['error'] = error_msg
            event_dict['bot_reply'] = True
        finally:
            pass

    # write databse
    event_dict['msg'] = msg
    print(event_dict)
    db.write(event_dict, DB)
    # if error keep another record too
    if 'error' in event_dict:
        db.write(event_dict, DB_ERR)

    # reply bot
    print(f'write to {DB}')
    if 'bot_reply' in event_dict or msg == '':
        if event_dict['bot_reply'] or msg == '':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))

    # manage bot leave
    if 'bot_action' in event_dict:
        if event_dict['bot_action'] == 'leave':
            if event.source.type == 'room':
                line_bot_api.leave_room(event.source.room_id)
            elif event.source.type == 'group':
                line_bot_api.leave_group(event.source.group_id)


@ handler.add(JoinEvent)
def handle_join(event):
    print(event.source)
    msg = CONST['greeting']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


@handler.default()
def default(event):
    event_dict = {}
    event_dict['timestamp'] = datetime.now(timezone.utc)
    event_dict['event'] = event.as_json_dict()
    db.write(event_dict, DB)


@app.get("/", include_in_schema=False)
async def root():
    # return {'message': "Hello welcome to Kampuan API (คำผวน)",
    #         'author': "Tanawat C."}
    response = RedirectResponse(url='/docs')
    return response


def check_if_list(text):
    return (text[0] == '[' and text[-1] == ']') or (',' in text)


def handle_white_spaces(text):
    text = re.sub(' +', ',', text)
    return text


def process_555(text: str):
    text = text.replace('5', 'ฮ่า')
    return text


def process_text_2_list(text):
    text = text.strip()
    text = handle_white_spaces(text)
    text = process_555(text)
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
    """Puan kum (ผวนคำ) is a Thai toung twister, This API convert string into kampuan
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
        raise HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)

    try:
        split_words = kp.puan_kam_preprocess(text, skip_tokenize=skip_tokenize)
    except ValueError as e:
        try:
            split_words = kp.puan_kam_preprocess(text, skip_tokenize=True)
        except ValueError as e:
            raise HTTPException(422, detail=f'Input error: {e}')

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
            skip_tokenize: Optional[bool] = None,
            translate_lu: Optional[bool] = False):
    """ภาษาลู

    -Args:
    - **text** (str):  Defaults to 'สวัสดี'.
        - input string 'ไปเที่ยว' -> auto tokenize will apply and split to ไป and  เที่ยว
        - list of string which accepted 3 formats: ['ไป','กิน','ข้าว'] | 'ไป','กิน','ข้าว' | ไป,กิน,ข้าว, the list input will also neglect auto tokenization.

    -Returns:
    - **results**: List of คำผันลู
    """
    if not check_thai_ch(text):
        raise HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)
    try:
        split_words = kp.puan_kam_preprocess(text, skip_tokenize=skip_tokenize)
    except ValueError as e:
        try:
            split_words = kp.puan_kam_preprocess(text, skip_tokenize=True)
        except ValueError as e:
            raise HTTPException(422, detail=f'Input error: {e}')

    if translate_lu:
        result = kp.translate_lu(text=split_words)
    else:
        result = kp.puan_lu(text=split_words)

    return {'input': text,
            'results': result}


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
        raise HTTPException(400, detail=f'Input contains non Thai')

    text = process_text_2_list(text)
    return {'input': text,
            'results': kp.pun_wunayook(text=text)}


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


# %%
