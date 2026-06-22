"""
Construit la base vectorielle depuis le CSV médical.
Lance une seule fois : python ingest.py
"""
import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from config import get_embeddings

load_dotenv()

# Étape 1 : lire et nettoyer le CSV
print("Lecture du CSV...")
df = pd.read_csv("data/medical_dataset_combined.csv")
df = df.dropna(subset=["question", "answer"]).drop_duplicates(subset=["question"])
df = df.sample(n=min(5000, len(df)), random_state=42)
print(f"{len(df)} lignes gardées")

# Étape 2 : créer les documents
docs = [
    Document(page_content=f"Question : {row['question']}\nRéponse : {row['answer']}")
    for _, row in df.iterrows()
]

# Étape 3 : découper en morceaux de 500 caractères
morceaux = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
print(f"{len(morceaux)} morceaux créés")

# Étape 4 : vectoriser et sauvegarder
print("Création des vecteurs (2-3 min)...")
index = FAISS.from_documents(morceaux, get_embeddings())
os.makedirs("data/faiss_index", exist_ok=True)
index.save_local("data/faiss_index")    

print(f"Terminé ! Index sauvegardé dans data/faiss_index/")
