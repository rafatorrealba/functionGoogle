from google.cloud import firestore
from datetime import datetime
import json

DB = firestore.Client()

def get_gtin(request):
    """
    Ésta función permite extraer el GTIN del json que viene de DialogFlow.
    A su vez, hace un llamado a la función de query con el GTIN como argumento.
    """
    request_json = request.get_json()
    number = str(int(request_json["queryResult"]["parameters"]["number"][0])) #Se extrae el dato importante de todo el json.
    gtin = number
    return query(gtin)

def query(gtin_number):
    """
    Esta función hace el query a la DB en Firestore, toma como argumento el GTIN.
    Retorna cuatro posibles mensajes dependiendo del estado de la garantía en la DB.
    """
    db_ref = DB.collection(u'dtcDB')                        #Hace referencia a la colección donde se encuentra la data en Firestore
    docs = db_ref.get()                                     #Con el metodo get se obtienen los datos.

    for doc in docs:                                        #Busca uno por uno los datos en "dtcDB"
        doc_dict = doc.to_dict()                            #Si hace algún match con el dato buscado, lo transforma a diccionario.
        gtin = doc_dict.get("GTIN").decode()                #Obtiene y decodifica el valor del GTIN en el diccionario.

        if gtin == gtin_number:                             #Si el dato decodificado es igual al GTIN del json 
            wdates = doc_dict.get("warrantyDate").decode()  #Se obtiene y decodifica el valor de la decha de la garantía.

            wdatet = datetime.strptime(wdates, "%Y/%m/%d")  #Se transforma el dato de la fecha a formato "timestamp"
            wdate = wdatet.date()                           #Se toma solo la fecha, se omite la hora.

            nowt = datetime.now()                           #Se obtiene el "timestamp" del momento de consulta.
            datenow = nowt.date()                           #Toma solo la fecha, se omite la hora.

            if wdate > datenow:                             #Se compara la fecha de la garantía con la de la fecha de consulta
                json_message = {}
                json_message["fulfillmentText"] = "¡Felicidades! La garantía número " + str(gtin_number) + " está ACTIVA ¿te gustaría planificar una cita para ser atendido por nuestro personal calificado?"
                return(json.dumps(json_message, ensure_ascii=False)) #Se entrega el mensaje en formato json.

            elif wdate < datenow:                           #Se compara la fecha de la garantía con la de la fecha de consulta
                json_message = {}
                json_message["fulfillmentText"] = "¡Lo siento! La garantía número " + str(gtin_number) + " está INACTIVA ¿te gustaría planificar una cita para ser atendido por nuestro personal calificado?"
                return(json.dumps(json_message, ensure_ascii=False)) #Se entrega el mensaje en formato json.

            elif wdate == datenow:                          #Se compara la fecha de la garantía con la de la fecha de consulta
                json_message = {}
                json_message["fulfillmentText"] = "¡Felicidades! La garantía número " + str(gtin_number) + " está ACTIVA y vence hoy, ¿te gustaría planificar una cita para ser atendido por nuestro personal calificado?"
                return(json.dumps(json_message, ensure_ascii=False)) #Se entrega el mensaje en formato json.
    json_message = {}
    json_message["fulfillmentText"] = "Lo sentimos, la garantía " + str(gtin_number) + " no está en nuestra base de datos"
    return(json.dumps(json_message, ensure_ascii=False))    #Se entrega el mensaje en formato json.
