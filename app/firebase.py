import firebase_admin
from firebase_admin import credentials, firestore


class FireBaseDb:
    def __init__(self, collection_name, credential_json="google-credentials.json"):
        self.db = collection_name
        cred = credentials.Certificate(credential_json)
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def test(self,):
        # read data
        snapshots = self.client.collection(self.db).get()
        print(snapshots[0].to_dict())

    def write(self, content, collection_name):
        self.client .collection(collection_name).add(content)


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

# test_firebase_function()
# db =FireBaseDb(u'test')
# db.test()
