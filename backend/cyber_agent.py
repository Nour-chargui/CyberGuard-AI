import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# 1. Définition des outils (Tools)
@tool
def analyze_vulnerability_level(description: str):
    """Calcule la dangerosité d'une faille de sécurité (Score CVSS)."""
    desc = description.lower()
    if any(kw in desc for kw in ["rce", "critique", "injection", "root"]):
        return "CRITIQUE (Score 9.8). Action : Isolement immédiat et coupure des accès réseaux."
    return "MOYEN (Score 5.0). Action : Analyse approfondie et correctif standard requis."

class CyberAgentExecutor:
    """
    CONCEPTION PERSONNALISÉE : Cette classe remplace AgentExecutor de LangChain.
    Elle gère manuellement la boucle de raisonnement et l'appel d'outils.
    """
    def __init__(self, rag_engine):
        self.llm = ChatGroq(
           temperature=0, 
           model_name="llama-3.3-70b-versatile", # C'est le nouveau nom du modèle puissant
           groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.rag = rag_engine
        # On lie les outils au modèle
        self.tools = [analyze_vulnerability_level, self.search_knowledge_base_tool]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def search_knowledge_base_tool(self, query: str):
        """Recherche des solutions dans la base de connaissances RAG."""
        results = self.rag.search(query)
        return "\n\n".join([r.page_content for r in results]) if results else "Pas de doc trouvé."

    def invoke(self, input_data):
        user_input = input_data["input"]
        
        # 1. Initialisation des messages
        messages = [
            SystemMessage(content="Tu es un expert Cyber SOC. Utilise tes outils pour aider l'utilisateur."),
            HumanMessage(content=user_input)
        ]

        # 2. Appel du LLM pour décider de l'action
        response = self.llm_with_tools.invoke(messages)
        
        # 3. Si l'IA veut utiliser des outils
        if response.tool_calls:
            messages.append(response)
            for tool_call in response.tool_calls:
                # Identification de l'outil à appeler
                if tool_call["name"] == "analyze_vulnerability_level":
                    tool_output = analyze_vulnerability_level.invoke(tool_call["args"])
                else:
                    tool_output = self.search_knowledge_base_tool(tool_call["args"].get("query", user_input))
                
                # Ajout du résultat de l'outil à la conversation
                messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))
            
            # 4. Appel final du LLM avec les résultats des outils
            final_response = self.llm_with_tools.invoke(messages)
            return {"output": final_response.content}
        
        return {"output": response.content}

def get_agent(rag_engine):
    """Retourne l'exécuteur d'agent personnalisé."""
    return CyberAgentExecutor(rag_engine)