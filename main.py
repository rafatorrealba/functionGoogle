from google.cloud import firestore
from datetime import datetime
import json

DB = firestore.Client()

def get_gtin(request):
    request_json = request.get_json()
    number = str(int(request_json["queryResult"]["parameters"]["number"][0]))
    gtin = number
    return query(gtin)

def query(gtin_number):

    db_ref = DB.collection(u'dtcDB')
    docs = db_ref.get()

    for doc in docs:
        doc_dict = doc.to_dict()
        gtin = doc_dict.get("GTIN").decode()

        if gtin == gtin_number:
            wdates = doc_dict.get("warrantyDate").decode()

            wdatet = datetime.strptime(wdates, "%Y/%m/%d")  
            wdate = wdatet.date()                           

            nowt = datetime.now()                           
            datenow = nowt.date()                           

            if wdate > datenow:                             
                json_message = {}
                json_message["fulfillmentText"] = "La garantía número " + str(gtin_number) + " está ACTIVA ¿te gustaría planificar una cita para ser atendido por nuestro personal calificado?"
                return(json.dumps(json_message, ensure_ascii=False))

            elif wdate < datenow:
                json_message = {}
                json_message["fulfillmentText"] = "La garantía número " + str(gtin_number) + " está INACTIVA"
                return(json.dumps(json_message, ensure_ascii=False))

            elif wdate == datenow:
                json_message = {}
                json_message["fulfillmentText"] = "La garantía número " + str(gtin_number) + " está ACTIVA y vence HOY ¿te gustaría planificar una cita para ser atendido por nuestro personal calificado?"
                return(json.dumps(json_message, ensure_ascii=False))
    json_message = {}
    json_message["fulfillmentText"] = "Lo sentimos, la garantía " + str(gtin_number) + " no está en nuestra base de datos"
    return(json.dumps(json_message, ensure_ascii=False))
