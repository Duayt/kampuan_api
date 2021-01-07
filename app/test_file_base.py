# %%
import firebase_admin
from firebase_admin import credentials, firestore
from linebot.models import (JoinEvent, MessageEvent, TextMessage,
                            TextSendMessage)
from datetime import datetime, timezone

credential_json = '../google-credentials.json'
cred = credentials.Certificate(credential_json)
firebase_admin.initialize_app(cred)


# %%
client = firestore.client()

# %%

source_user = {
    'userId': 'poom',
    'type': 'user'
}

source_group = {
    'groupId': 'poom_groupid',
    'type': 'group',
    'userId': 'poom'
}


source_room = {
    'roomId': 'poom_roomid',
    'type': 'room',
    'userId': 'poom'
}

source_info = {
    'bot_config': 'abc',
    'sources': '123',
    'source_sessions': 'a'
}
mock_msg_0 = {
    'id': "13311178697299",
    "text": "mock_msg_0",
    "type": 'text'
}

mock_msg_1 = {
    'id': "133111786972123",
    "text": "mock_msg_1",
    "type": 'text'
}

mock_src = source_group


# result = client.collection(
#     'groups', 'source', src['type']).add(src, src['userId'])


def add_to_collection(client, collection_path, content, id):
    return client.collection(*collection_path).add(content, id)


def get_source_info():
    return {'member': 4,
            'group_name': 'test'}


def get_source_id(src):
    if src.type == 'user':
        return src.user_id
    elif src.type == 'group':
        return src.group_id
    elif src.type == 'room':
        return src.room_id


def collect_source(client, src, src_info, source_id):
    return client.collection('groups',
                             'source',
                             src.type).add({'source': src.as_json_dict(),
                                            'source_info': src_info},
                                           source_id)

    # return add_to_collection(client, collection_path=(
    #     'groups', 'source', src.type), content={'source': src.as_json_dict(),
    #                                             'source_info': src_info}, id=source_id)


def collect_doc(client,
                content,
                source_id,
                collection_name,
                collection_sub_name, content_id=None):
    return client.collection(collection_name).\
        document(source_id).\
        collection(collection_sub_name).add(content, content_id)


def collect_event(client, event_dict, source_id):
    return collect_doc(client, event_dict, source_id, 'events', 'events')


def collect_msg(client, msg_dict, source_id, msg_id=None):
    return collect_doc(client, msg_dict, source_id, 'messages', 'messages', msg_id)


def collect_bot_reply(client, msg_dict, source_id):
    return collect_doc(client, msg_dict, source_id, 'messages', 'bot_reply')


def get_latest_msg(client, source_id):
    return client.collection('messages').document(source_id).collection('messages').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)


# %%
# user submit event
mock_event_0 = MessageEvent(
    mode='active', timestamp='1', source=source_group, reply_token='test', message=mock_msg_0)

# collect new/update source
source_info = get_source_info()

# join event
# collect groupinfo
get_source_id(mock_event_0.source)

source_id = get_source_id(mock_event_0.source)

try:
    source_doc_ref = collect_source(
        client, mock_event_0.source, source_info, source_id)
except:
    print('exist')


# collect new events with sourceid/session id
collect_event(client, mock_event_0.as_json_dict(), source_id)
# collect new msg with sourceid/session id
# %%
for i in range(10):
    mock_msg = {
        'id': str(i)*10,
        "text": f"mock_msg_1{i}",
        "type": 'text'
    }

    collect_msg(client, {'message': mock_msg, 'timestamp': datetime.now(timezone.utc)
                         }, source_id, mock_msg['id'])


# get previous msg within the session id

# reply with previous msg


# %%
# check source_id
def check_source(source_id):
    return client.collection('groups').document(
        'source').collection('group').document(source_id).get().exists
