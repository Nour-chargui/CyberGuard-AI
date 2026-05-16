import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import de tes modules personnalisés
from rag_engine import SecureRAGEngine
from cyber_agent import get_agent

# 1. Chargement des variables d'environnement (.env) dès le début
load_dotenv()

# 2. Initialisation des composants globaux
# On les crée ici pour qu'ils soient accessibles partout
rag = SecureRAGEngine()
agent_executor = get_agent(rag)

# --- SYSTÈME DE DÉMARRAGE MODERNE (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gère le démarrage et l'arrêt de l'application.
    Idéal pour l'indexation initiale du RAG.
    """
    print("🚀 Initialisation du SOC CyberGuard...")
    
    # Création d'un fichier de connaissances par défaut si inexistant
    if not os.path.exists("cyber_docs.txt"):
        with open("cyber_docs.txt", "w", encoding="utf-8") as f:
            f.write("Note: Les attaques par Brute Force sur le port 22 (SSH) sont critiques. \n")
            f.write("Conseil: Désactiver l'accès root et utiliser exclusivement des clés SSH RSA 4096 bits.")
    
    # Ingestion des documents dans la base vectorielle ChromaDB
    try:
        rag.ingest_document("cyber_docs.txt")
        print("✅ Base de connaissances (RAG) indexée avec succès.")
        print("✅ Agent IA Groq (Llama 3) opérationnel.")
        print("🌍 Serveur prêt sur http://localhost:8000")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du RAG : {e}")
        
    yield
    # Code à exécuter lors de l'arrêt du serveur
    print("🛑 Arrêt du système CyberGuard...")

# 3. Création de l'application FastAPI
app = FastAPI(
    title="CyberGuard AI - API",
    description="Backend de cybersécurité piloté par IA",
    lifespan=lifespan
)

# 4. Configuration du middleware CORS (Autorise le Frontend React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, remplacer par l'URL de ton front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Modèle de données pour les requêtes entrantes
class ChatInput(BaseModel):
    message: str

# 6. Endpoint principal pour le Chat
@app.post("/api/chat")
async def chat_endpoint(data: ChatInput):
    """
    Reçoit le message utilisateur, l'envoie à l'agent et renvoie la réponse.
    """
    try:
        # Appel de l'agent (LangChain AgentExecutor)
        result = agent_executor.invoke({"input": data.message})
        return {"response": result["output"]}
    except Exception as e:
        print(f"⚠️ Erreur lors du traitement du message : {e}")
        return {"response": f"Désolé, le SOC rencontre une erreur technique : {str(e)}"}

# 7. Lancement du serveur
if __name__ == "__main__":
    import uvicorn
    # On lance uvicorn sur le port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)