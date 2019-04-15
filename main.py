'''
Ésta función permite hacer el Query a la DB en Firestore.
Puede configurarse para hacer query a toda la collección
o para hacer query a una parte determinada.

This function allows querying the Firestore DB.
May be configured to querying all collection or
just a part of it.
'''

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()
print("Initializing...")

# Query against a part of the collection
docs = db.collection(u'test').where(u'warrantyStatus', u'==', 'Active').get()

#Query against all collection
#docs = db.collection(u'test').get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
