'''
Ésta función permite hacer el Query a la DB en Firestore.
Puede configurarse para hacer query a toda la collección
o para hacer query a una parte determinada y mostrar el 
estado activo o inactivo de la garantía.

This function allows querying the Firestore DB.
May be configured to querying all collection or
just a part of it and show an active or inactive
state of warranty.
'''

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()
print("Initializing...")

#Query against all collection
#docs = db.collection(u'dtcDB').limit(10).get()

#Query against a part of the collection
docs = db.collection(u'dtcDB').where(u'GTIN', u'==', '10637').get()

#Print specific data
for doc in docs:
    dict = doc.to_dict()
    wdates = dict.get("warrantyDate")

    wdatet = datetime.strptime(wdates, "%Y/%m/%d")  #Transfor warrantyDate from strig to timestamp
    wdate = wdatet.date()                           #Take just the date of warrantyDate

    nowt = datetime.now()                           #Timestam of today
    datenow = nowt.date()                           #Take just the date of today

    if wdate < datenow:                             #Date comparation
        print("Your warranty is inactive")          #Inactive warrranty
    elif wdate > datenow:
        print("Your warranty is active")            #Active warrranty
    elif wdate == datenow:
        print("Your warranty ends today")           #Warranty ends today

#Print all data
#for doc in docs:
    #print("Your id invoice is " '"{}" \nAnd your data is: {}'.format(doc.id, doc.to_dict()))
