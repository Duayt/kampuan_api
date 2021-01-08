# %%
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone


def get_source_id(src):
    if src.type == 'user':
        return src.user_id
    elif src.type == 'group':
        return src.group_id
    elif src.type == 'room':
        return src.room_id


class FireBaseDb:
    def __init__(self,
                 credential_json="google-credentials.json",
                 env='test_bot'):
        cred = credentials.Certificate(credential_json)
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        self.env = env
    # def test(self,):
    #     # read data
    #     snapshots = self.client.collection(self.db).get()
    #     print(snapshots[0].to_dict())

    def write(self, content, collection_name):
        self.client.collection(collection_name).add(content)

    def collect_source(self, src, src_info):
        print(f'collecting source {src_info}')
        return self.client.collection('groups', self.env, src.type).\
            add({'source': src.as_json_dict(),
                 'source_info': src_info,
                 'timestamp': datetime.now(timezone.utc)},
                get_source_id(src))

    def set_source(self, src, src_info):
        return self.client.collection('groups', self.env, src.type).\
            document(get_source_id(src)).set({'source': src.as_json_dict(),
                                              'source_info': src_info,
                                              'timestamp': datetime.now(timezone.utc)},
                                             )

    def get_doc(self,
                source_id,
                collection_name,
                collection_sub_name):
        return self.client.collection(collection_name).\
            document(source_id).\
            collection(collection_sub_name)

    def collect_doc(self,
                    content,
                    source_id,
                    collection_name,
                    collection_sub_name,
                    content_id=None):
        content['timestamp'] = datetime.now(timezone.utc)
        return self.get_doc(source_id=source_id,
                            collection_name=collection_name,
                            collection_sub_name=collection_sub_name).\
            add(content, content_id)

    def update_doc(self,
                   content,
                   source_id,
                   collection_name,
                   collection_sub_name,
                   content_id=None):
        content['timestamp'] = datetime.now(timezone.utc)
        return self.get_doc(source_id=source_id,
                            collection_name=collection_name,
                            collection_sub_name=collection_sub_name).\
            document(content_id).update(content)

    def check_doc(self,
                  content_id,
                  source_id,
                  collection_name,
                  collection_sub_name,):
        return self.get_doc(source_id=source_id,
                            collection_name=collection_name,
                            collection_sub_name=collection_sub_name).\
            document(content_id).get().exists

    def collect_event(self, event_dict, source):

        return self.collect_doc(content=event_dict,
                                source_id=get_source_id(source),
                                collection_name='events',
                                collection_sub_name=self.env)

    def collect_msg(self,
                    msg_dict,
                    source,
                    msg_id=None):
        return self.collect_doc(content=msg_dict,
                                source_id=get_source_id(source),
                                collection_name='messages',
                                collection_sub_name=self.env,
                                content_id=msg_id)

    def check_usr(self,
                  profile,
                  source):
        return self.check_doc(source_id=get_source_id(source),
                              collection_name='users',
                              collection_sub_name=self.env,
                              content_id=profile.user_id)

    def update_usr(self,
                   profile,
                   source):
        return self.update_doc(content=profile.as_json_dict(),
                               source_id=get_source_id(source),
                               collection_name='users',
                               collection_sub_name=self.env,
                               content_id=profile.user_id)

    def collect_usr(self,
                    profile,
                    source):
        if self.check_usr(profile=profile, source=source):
            return self.update_usr(profile=profile, source=source)
        else:
            return self.collect_doc(content=profile.as_json_dict(),
                                    source_id=get_source_id(source),
                                    collection_name='users',
                                    collection_sub_name=self.env,
                                    content_id=profile.user_id)

    def collect_bot_reply(self,
                          msg_dict,
                          source,
                          msg_id=None):
        return self.collect_doc(content=msg_dict,
                                source_id=get_source_id(source),
                                collection_name='messages',
                                collection_sub_name=self.env + '_bot_reply',
                                content_id=msg_id)

    def get_latest_msg_query(self, source):
        return self.client.collection('messages').\
            document(get_source_id(source)).collection(self.env).\
            order_by('timestamp', direction=firestore.Query.DESCENDING).\
            limit(1)

    def get_latest_msg(self, source, msg_if_none=False):
        query = self.get_latest_msg_query(source).get()

        if not query:
            return msg_if_none
        else:
            return query[0].to_dict()['msg']['text']

    def check_source(self, source):
        return self.client.collection('groups').\
            document(self.env).collection(source.type).\
            document(get_source_id(source)).get().exists

    def get_source_auto_config(self, source):
        query = self.client.collection('groups').\
            document(self.env).collection(source.type).\
            document(get_source_id(source)).get()

        if not query:
            print('source error')
            return False
        else:
            return query.to_dict()['source_info']['auto_mode']

    def update_source_info(self, source, source_info):
        return self.client.collection('groups', self.env, source.type).\
            document(get_source_id(source)).update(source_info)


def test_firebase_function(credential_json="google-credentials.json"):
    # initialize sdk
    cred = credentials.Certificate(credential_json)
    # initialize firestore instance
    firebase_admin.initialize_app(cred)
    firestore_db = firestore.client()

    # read data
    snapshots = list(firestore_db.collection(u'test').get())
    for snapshot in snapshots:
        print(snapshot.to_dict())


# %%
# db = FireBaseDb(credential_json='../google-credentials.json')

# #%%
# db.client.collection('groups', 'test', 'user').\
#     add({'source': 'test',
#          'source_info': {'auto_mode': True},
#          'timestamp': datetime.now(timezone.utc)},
#         'test_id')

# db.client.collection('groups', 'test', 'user').document(
#     'test_id').update({'source': 'sdf'})


# db.client.collection('groups', 'test', 'user').\
#     document('test_id').get().to_dict()['source_info']['auto_mode']
