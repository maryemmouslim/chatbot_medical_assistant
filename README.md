# Assistant d'Information Médicale

API FastAPI avec cache Redis et mémoire de conversation.
Le RAG (recherche dans une base de documents) est prévu pour l'étape suivante.

## Prérequis

- Python 3.11+
- Docker (pour lancer Redis facilement)

## 1. Lancer Redis avec Docker

```bash
docker run -d --name redis-medical -p 6379:6379 redis:7
```

## 2. Installer les dépendances Python

```bash
cd medical_assistant
pip install -r requirements.txt
```

## 3. Configurer les variables d'environnement

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer .env et remplir OPENAI_API_KEY (ou ANTHROPIC_API_KEY)
```

## 4. Lancer le serveur

```bash
uvicorn app:app --reload
```

L'API est accessible sur http://localhost:8000
La documentation interactive est sur http://localhost:8000/docs

---

## Tester que le cache fonctionne

### Première fois → source "llm" (appel au LLM, lent)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Quels sont les symptomes de la grippe ?\"}"
```

Réponse attendue :
```json
{
  "reponse": "Les symptômes de la grippe incluent...",
  "source": "llm",
  "duree_s": 2.1
}
```

### Deuxième fois (même question) → source "cache" (instantané)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Quels sont les symptomes de la grippe ?\"}"
```

Réponse attendue :
```json
{
  "reponse": "Les symptômes de la grippe incluent...",
  "source": "cache",
  "duree_s": 0.001
}
```

La `source` passe de `"llm"` à `"cache"` et `duree_s` chute drastiquement.

---

## Structure du projet

```
medical_assistant/
├── config.py        # Variables d'env + création du LLM
├── redis_client.py  # Connexion Redis partagée
├── cache.py         # Cache exact-match des réponses (TTL 7 jours)
├── memory.py        # Historique de conversation par session
├── pipeline.py      # Logique principale : cache → RAG stub → LLM
├── app.py           # Serveur FastAPI (POST /ask, GET /)
├── requirements.txt
├── .env.example
└── README.md
```

## Endpoints

| Méthode | URL   | Description                        |
|---------|-------|------------------------------------|
| GET     | /     | Health check (vérifie Redis)       |
| POST    | /ask  | Poser une question médicale        |

### Corps de la requête POST /ask

```json
{
  "question": "Quels sont les symptômes du diabète ?",
  "session_id": "user_123"
}
```
