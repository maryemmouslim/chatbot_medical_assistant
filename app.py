from fastapi import FastAPI
from pydantic import BaseModel
from redis_client import ping
from pipeline import repondre

app = FastAPI()


class Question(BaseModel):
    question: str
    session_id: str = "default"


@app.get("/")
def sante():
    return {"statut": "ok", "redis": ping()}


@app.post("/ask")
def poser_question(body: Question):
    try:
        return repondre(body.question, body.session_id)
    except Exception as e:
        return {"erreur": str(e), "type": type(e).__name__}
