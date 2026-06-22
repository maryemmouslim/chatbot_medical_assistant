import os
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from config import get_embeddings

load_dotenv()

SEUIL = 0.5  # score minimum pour qu'un résultat soit gardé

modele = get_embeddings()

# Charge l'index au démarrage s'il existe
index = None
if os.path.exists("data/faiss_index"):
    index = FAISS.load_local("data/faiss_index", modele, allow_dangerous_deserialization=True)
    print("Base médicale chargée.")
else:
    print("Pas d'index. Lance : python ingest.py")

def rechercher(question):
    if index is None:
        return None

    resultats = index.similarity_search_with_relevance_scores(question, k=3)
    passages = [doc.page_content for doc, score in resultats if score >= SEUIL]

    return "\n\n".join(passages) if passages else None
