from config import ENDEE_URL, INDEX_NAME

try:
    from endee import Endee
    # Initialize Endee client
    client = Endee()
    client.set_base_url(f"{ENDEE_URL}/api/v1")
except ImportError:
    client = None


def insert_vector(vector, text, vector_id=None):
    """
    Insert a single vector into the Endee index with optional unique ID.

    Args:
        vector: Embedding vector.
        text: Text associated with the vector.
        vector_id: Unique identifier.
    """
    if client is None:
        print("[stub] insert_vector called, but Endee client unavailable")
        return
    index = client.get_index(INDEX_NAME)
    vector_id = vector_id or str(hash(text))  

    index.upsert([
        {
            "id": vector_id,
            "vector": vector,
            "meta": {"text": text}
        }
    ])
    print(f"Inserted vector: {vector_id}")


def search_vector(vector, top_k=3):
    """
    Search the Endee index for similar vectors

    Args:
        vector: Query embedding vector.
        top_k: Number of top matches to return.

    Returns:
        dict: {"matches": [{"id": str, "score": float, "metadata": dict},...]}
    """
    if client is None:
        return {"matches": []}

    index = client.get_index(INDEX_NAME)
    
    # Query index
    response = index.query(
        vector=vector,
        top_k=top_k,
        include_vectors=False 
    )

    # Convert JSON format
    matches = []
    for item in response:
        matches.append({
            "id": item.get("id"),
            "score": item.get("similarity", 0.0),
            "metadata": item.get("meta", {})
        })

    return {"matches": matches}

