import os
import re
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class SecureRAGEngine:
    def __init__(self):
        # Initialisation des embeddings locaux
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.persist_directory = "./chroma_db"

    def anonymize_text(self, text: str) -> str:
        # Masquage des adresses IP IPv4
        text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "[IP_HIDDEN]", text)
        # Masquage des adresses emails
        text = re.sub(r'\S+@\S+', "[EMAIL_HIDDEN]", text)
        return text

    def ingest_document(self, file_path: str):
        """
        Charge et indexe le document cyber_docs.txt
        """
        # On s'assure d'utiliser le chemin absolu
        abs_path = os.path.abspath(file_path)
        
        if not os.path.exists(abs_path):
            # Création automatique du fichier s'il manque
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write("Note technique: Sécurisation du protocole SSH.\n")
                f.write("1. Désactiver l'authentification par mot de passe.\n")
                f.write("2. Utiliser des clés RSA de 4096 bits minimum.\n")
                f.write("3. Changer le port par défaut (22) pour limiter les scans automatisés.")

        try:
            # Lecture manuelle avec encodage sécurisé
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Application de l'anonymisation
            clean_text = self.anonymize_text(content)
            
            # Création du format Document pour LangChain
            doc = Document(page_content=clean_text, metadata={"source": abs_path})
            
            # Découpage en morceaux (chunks)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_documents([doc])
            
            # Création/Mise à jour de la base vectorielle ChromaDB
            self.vector_store = Chroma.from_documents(
                documents=chunks, 
                embedding=self.embeddings, 
                persist_directory=self.persist_directory
            )
            return "Succès : Document indexé."
        except Exception as e:
            print(f"❌ Erreur RAG détaillée : {str(e)}")
            return str(e)

    def search(self, query: str):
        if not self.vector_store:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory, 
                    embedding_function=self.embeddings
                )
            else:
                return []
        
        return self.vector_store.similarity_search(query, k=2)