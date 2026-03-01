from vectorstore.endee_client import search_vector
from sentence_transformers import SentenceTransformer

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

query = "How often is company policy reviewed?"
query_vector = model.encode(query).tolist()

print(f"Searching for query: {query}\n")

results = search_vector(query_vector)

for i, match in enumerate(results.get("matches", []), 1):
    text = match["metadata"].get("text", "")
    score = match["score"]
    vid = match["id"]
    print(f"{i}. ID: {vid}, Similarity: {score:.4f}")
    print(f"   Text: {text}\n")