# %%
import os
from datetime import datetime, timezone
from typing import Optional

import kampuan as kp
from fastapi import FastAPI, HTTPException, Request
from kampuan.lang_tools import process_text_2_list
# from starlette.requests import Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (JoinEvent, MessageEvent, TextMessage,
                            TextSendMessage)
from starlette.responses import RedirectResponse

from .const import ALL_CONST, BotCommand
from .firebase import FireBaseDb
from .util import SourceInfo

# variables
ENV = str(os.getenv('ENV', 'test'))

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
              description="Welcome,This is a project using python to do คำผวน by Tanawat C. ",
              version="0.0.1",)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
db = FireBaseDb(credential_json=GOOGLE_APPLICATION_CREDENTIALS, env=ENV)
# db.test()
bot_info = line_bot_api.get_bot_info()

bot_command = BotCommand(bot_name=bot_info.display_name, bot_env=ENV)
# %%


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


def handle_message_puan(text):
    # puan process usage
    use_first = text.strip().startswith('@')
    text = text.replace('@', '')
    puan_result = puan_kam(text=text, skip_tokenize=True, first=use_first)
    puan_result['msg'] = ''.join(puan_result['results'])
    return puan_result


def handle_message_pun(text):
    puan_result = {}
    puan_result = pun_wunnayook(text=text, skip_tokenize=True)
    puan_result['msg'] = '\n'.join([' '.join(pun)
                                    for k, pun in puan_result['results'].items()])
    return puan_result


def handle_message_lu(text):
    translate_lu = text.strip().startswith('@')
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

    # handle previous room
    if db.check_source(event.source):
        pass
    else:
        print('new room')
        db.collect_source(event.source, SourceInfo.old(ENV).to_dict())
    text = event.message.text.lower().strip()

    # data to text
    try:
        profile = line_bot_api.get_profile(event.source.user_id)
        db.collect_usr(profile=profile, source=event.source)
        print(profile.display_name)
        user_not_follow = False
    except Exception as e:
        if event.source.type == 'room':
            profile = line_bot_api.get_group_member_profile(
                event.source.room_id, event.source.user_id)
        else:
            profile = line_bot_api.get_room_member_profile(
                event.source.group_id, event.source.user_id)

        print(profile.display_name)
        print(e, 'user not follow')
        user_not_follow = True
        pass

    event_dict = {}
    event_dict['event'] = event.as_json_dict()
    msg_dict = {}
    msg_dict['msg'] = event.message.as_json_dict()
    auto_mode = db.get_source_auto_config(event.source)
    latest_msg = db.get_latest_msg(source=event.source)
    # handle testing functions
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
    event_dict['bot_reply'] = False
    # bot flow
    if user_not_follow:
        msg = reply_howto()
        event_dict['bot_reply'] = False
    elif text == '#'+str(bot_info.display_name):  # show manual
        msg = bot_command.reply_how_to
        event_dict['bot_reply'] = True

    elif text == bot_command.com_hi:
        msg = bot_command.reply_greeting
        event_dict['bot_reply'] = True

    elif text == bot_command.com_kick:
        if event.source.type == 'user':
            msg = bot_command.reply_kick_user_room
            event_dict['bot_reply'] = True
        else:
            msg = bot_command.reply_kick
            event_dict['bot_action'] = 'leave'
            event_dict['bot_reply'] = True

    elif text == bot_command.com_echo:
        msg = db.get_latest_msg(source=event.source, msg_if_none='no history')
        event_dict['bot_reply'] = True

   # toggle auto mode

    elif text == bot_command.com_auto:
        db.update_source_info(
            event.source, {'source_info': {'auto_mode': not(auto_mode)}})
        msg = bot_command.reply_auto_mode(auto_mode=auto_mode)
        event_dict['bot_reply'] = True

    # elif text.startswith('#'):
    #     pass

    else:
        # main puan logic
        # check if auto mode
        text_to_puan = False

        if ENV in ['test', 'lu', 'puan']:
            check_case = (text == CONST['exec']) or (
                text == CONST['exec_anti'])
        else:
            check_case = text == CONST['exec']

        if check_case:
            text_to_puan = latest_msg
            if ENV in ['test', 'lu', 'puan']:
                if text == CONST['exec_anti']:
                    text_to_puan = '@'+text_to_puan
            # puan process usage
            if text_to_puan:
                event_dict['text_to_puan'] = text_to_puan
                event_dict['bot_reply'] = True
                try:
                    puan_result = handle_funct(text_to_puan)
                    msg = puan_result['msg']
                    event_dict['puan_result'] = puan_result
                except Exception as e:
                    if text_to_puan.startswith("#"):
                        msg = bot_command.reply_error_text_for_action(
                            text_to_puan)
                    else:
                        msg = bot_command.reply_error_text(text_to_puan)
                    error_msg = f'{str(repr(e))}'
                    print(error_msg)
                    event_dict['error'] = error_msg
                finally:
                    pass
            else:
                msg = bot_command.reply_no_history
                print('no history')
                event_dict['bot_reply'] = True

        # check if execution phrase
        elif auto_mode:
            print('auto mode')
            text_to_puan = text
        # puan process
            event_dict['text_to_puan'] = text_to_puan
            event_dict['bot_reply'] = True
            try:
                puan_result = handle_funct(text_to_puan)
                msg = puan_result['msg']
                event_dict['puan_result'] = puan_result
            except Exception as e:
                if text_to_puan.startswith("#"):
                    msg = bot_command.reply_error_text_for_action(text_to_puan)
                else:
                    msg = bot_command.reply_error_text(text_to_puan)
                error_msg = f'{str(repr(e))}'
                print(error_msg)
                event_dict['error'] = error_msg
            finally:
                pass
    # write
    event_dict['msg'] = msg
    print(event_dict)
    db.collect_event(
        event_dict=event_dict,
        source=event.source)

    db.collect_msg(msg_dict=msg_dict, source=event.source,
                   msg_id=event.message.id)
    # if error keep another record too
    if 'error' in event_dict:
        db.write(event_dict, DB_ERR)

    # reply bot
    print(f'write to {DB}')
    if 'bot_reply' in event_dict:
        if event_dict['bot_reply']:
            # collect bot reply as msg too
            db.collect_msg(msg_dict={'msg': {'text': msg}, 'type': 'bot'},
                           source=event.source,
                           msg_id=event.message.id+"_bot")

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
    try:
        profile = line_bot_api.get_profile(event.source.user_id)
        db.collect_usr(profile=profile, source=event.source)
        print(profile.display_name)
    except Exception as e:
        print(e)
        pass

    if db.check_source(event.source):
        db.set_source(event.source, SourceInfo.rejoin(ENV).to_dict())
    else:
        db.collect_source(event.source, SourceInfo.new(ENV).to_dict())

    msg = bot_command.reply_greeting
    db.collect_event(
        event_dict={'event': event.as_json_dict(),
                    'msg': msg},
        source=event.source)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


@handler.default()
def default(event):
    # db.write(event_dict, DB)
    if db.check_source(event.source):
        pass
    else:
        db.collect_source(event.source,  SourceInfo.old(ENV).to_dict())
    try:
        profile = line_bot_api.get_profile(event.source.user_id)
        db.collect_usr(profile=profile, source=event.source)
        print(profile.display_name)
    except Exception as e:
        print(e)
        pass
    print(type(event))
    print(event.as_json_dict())
    db.collect_event(
        event_dict={'event': event.as_json_dict()},
        source=event.source)


#### API #####

@app.get("/", include_in_schema=False)
async def root():
    # return {'message': "Hello welcome to Kampuan API (คำผวน)",
    #         'author': "Tanawat C."}
    response = RedirectResponse(url='/docs')
    return response


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
    except ValueError:
        try:
            split_words = kp.puan_kam_preprocess(
                text, skip_tokenize=not(skip_tokenize))
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
        split_words = kp.puan_kam_preprocess(
            text, skip_tokenize=skip_tokenize, flag_lu_2_thai=translate_lu)
    except ValueError:
        try:
            split_words = kp.puan_kam_preprocess(
                text, skip_tokenize=not(skip_tokenize), flag_lu_2_thai=translate_lu)
        except ValueError as e:
            raise HTTPException(422, detail=f'Input error: {e}')

    if translate_lu:
        result = kp.translate_lu(text=split_words)
    else:
        result = kp.puan_lu(text=split_words)

    return {'input': text,
            'results': result}


@app.get("/pun_wunnayook/{text}")
def pun_wunnayook(text: str = 'สวัสดี',
                  skip_tokenize: Optional[bool] = None):
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
    try:
        split_words = kp.puan_kam_preprocess(
            text, skip_tokenize=skip_tokenize)
    except ValueError:
        try:
            split_words = kp.puan_kam_preprocess(
                text, skip_tokenize=not(skip_tokenize))

        except ValueError as e:
            raise HTTPException(422, detail=f'Input error: {e}')

    return {'input': text,
            'results': kp.pun_wunayook(text=split_words)}


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

# %%
