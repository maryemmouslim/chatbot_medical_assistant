import json
from redis_client import client

def get_historique(session_id):
    entrees = client.lrange("memory:" + session_id, 0, -1)
    return [json.loads(e) for e in entrees]

def ajouter_echange(session_id, question, reponse):
    cle = "memory:" + session_id
    client.rpush(cle, json.dumps({"question": question, "reponse": reponse}))
    client.ltrim(cle, -10, -1)  # garde les 10 derniers
