from redis_client import client

TTL = 7 * 24 * 60 * 60  # 7 jours

def get_reponse_cache(question):
    return client.get("cache:" + question.strip().lower())

def set_reponse_cache(question, reponse):
    client.set("cache:" + question.strip().lower(), reponse, ex=TTL)
