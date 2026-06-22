import time
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from config import get_llm
from cache import get_reponse_cache, set_reponse_cache
from memory import get_historique, ajouter_echange
from rag import rechercher

llm = get_llm()

PROMPT = """Tu es un assistant médical prudent.
Réponds UNIQUEMENT à partir du contexte ci-dessous.
Si le contexte ne suffit pas, dis "je ne sais pas".
Rappelle que tu ne remplaces pas un médecin.

Contexte :
{contexte}"""

def repondre(question, session_id="default"):
    debut = time.time()

    # 1. Cache : réponse déjà connue ?
    reponse = get_reponse_cache(question)
    if reponse:
        return {"reponse": reponse, "source": "cache", "duree_s": round(time.time() - debut, 4)}

    # 2. RAG : chercher dans la base médicale
    contexte = rechercher(question)

    # 3. Rien trouvé → refus d'inventer
    if contexte is None:
        return {"reponse": "Je n'ai pas cette information dans ma base.", "source": "hors_base", "duree_s": round(time.time() - debut, 4)}

    # 4. LLM : rédiger la réponse avec le contexte
    messages = [SystemMessage(content=PROMPT.format(contexte=contexte))]
    for e in get_historique(session_id):
        messages += [HumanMessage(content=e["question"]), AIMessage(content=e["reponse"])]
    messages.append(HumanMessage(content=question))

    reponse = llm.invoke(messages).content

    # 5. Sauvegarder
    set_reponse_cache(question, reponse)
    ajouter_echange(session_id, question, reponse)

    return {"reponse": reponse, "source": "llm", "duree_s": round(time.time() - debut, 4)}
