# vectorstore/rag_tool.py
#import os
try:
    from vectorstore.endee_client import search_vector
except ImportError:
    search_vector = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

from config import GEMINI_API_KEY

# lazy-loading 
_embedding_model = None

def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        except ImportError:
            # dummy model that returns zero vectors if sentence_transformers is not available
            class Dummy:
                def encode(self, text):
                    return [0.0] * 384
            _embedding_model = Dummy()
    return _embedding_model

# Initialize LLM if available
if ChatGoogleGenerativeAI is not None:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )
else:
    llm = None

def rag_search(query, top_k=3):
    """
    Perform RAG search:
    - Embed query
    - Retrieve top_k vectors from Endee
    - Generate answer using Gemini LLM
    Returns a JSON dict with query, matches, and LLM answer
    """
    # Step 1: Embed query
    model = _get_embedding_model()
    emb = model.encode(query)
    # if the embedding is a numpy array or has tolist, convert, else assume it's a list
    if hasattr(emb, "tolist"):
        query_embedding = emb.tolist()
    else:
        query_embedding = list(emb)

    # Step 2: Search Endee 
    matches = []
    if search_vector is not None:
        try:
            results = search_vector(query_embedding, top_k=top_k)
            matches = results.get("matches", [])
        except Exception:
            matches = []

    # Prepare context and match info
    context_list = []
    match_info = []

    for match in matches:
        metadata = match.get("metadata", {})
        text = metadata.get("text", "")
        similarity = match.get("score", 0.0) # similarity score from Endee

        if text:
            context_list.append(text)
            match_info.append({
                "text": text,
                "similarity": similarity
            })

    context = "\n".join(context_list) if context_list else "No HR policy context found."

    # Step 3: Generate answer with Gemini
    answer = ""
    if llm is not None:
        prompt = f"""
You are an Enterprise HR Assistant.

Answer strictly using the HR policy context below.

Context:
{context}

Question:
{query}

Answer professionally and clearly.
"""
        response = llm.invoke(prompt)
        answer = response.content
    else:
        answer = "(LLM not available in this environment)"

    # Step 4: Construct output JSON
    output = {
        "query": query,
        "top_matches": match_info,
        "answer": answer
    }

    # Debug prints
    print("\nQuerying RAG pipeline:")
    print(query)
    print("\nTop matches:")
    for i, m in enumerate(match_info, 1):
        print(f"{i}. Text: {m['text']}")
        print(f"   Similarity: {m['similarity']:.4f}")

    print("\nRAG-generated response:\n")
    print(answer)

    return output