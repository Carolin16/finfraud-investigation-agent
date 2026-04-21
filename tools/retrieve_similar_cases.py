from langchain_core.tools import tool
from rag import RAGExplainer

# loads ChromaDB once at import time
rag =  RAGExplainer()

@tool
def retrieve_similar_cases(query : str) -> str:
    """
        Search the internal case database for historical fraud cases 
        similar to the current invoice. Use this when you need precedent 
        for a fraud pattern you have identified. Input should be a plain 
        English description of the suspicious pattern.
    
    """
    results = rag.retrieve_similar(query)
    if not results :
        return "No similar cases found in the database."
    
    return "\n---\n".join(results)
