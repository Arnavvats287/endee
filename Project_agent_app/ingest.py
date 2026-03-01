import json
from sentence_transformers import SentenceTransformer
from vectorstore.endee_client import insert_vector  

# Load  model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

dataset_path = "data/hr_dataset.jsonl"

with open(dataset_path, "r", encoding="utf-8") as f:
    count = 0
    for line in f:
        data = json.loads(line)
        messages = data.get("messages", [])
        for msg in messages:
            if msg.get("role") == "assistant":
                text = msg.get("content")
                embedding = model.encode(text).tolist()
                insert_vector(embedding, text)
                count += 1

print(f"Ingestion complete. {count} vectors inserted.")