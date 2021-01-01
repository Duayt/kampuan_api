import firebase_admin
from firebase_admin import credentials, firestore


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

    # write data
    # content = {"events": [{"type": "message", "replyToken": "cf4b97eaff1f4439b42d944876227705", "source": {"userId": "U787965c323ccfdc033284a4da7a0f06c", "type": "user"},
    #                        "timestamp": 1609434096323, "mode": "active", "message": {"type": "text", "id": "13302063883530", "text": "สวัสดีปีใหม่"}}], "destination": "Ua87f56072aab1ce8989c2450890bf4e0"}
    # firestore_db.collection(u'test').add(content)

# test_firebase_function()
