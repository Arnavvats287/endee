from vectorstore.endee_client import insert_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Dummy texts
dummy_texts = [
    "Employees will receive annual performance reviews.",
    "The company policy is reviewed every year to ensure compliance.",
    "Employees should report any safety incidents immediately.",
]

print("Inserting dummy vectors into Endee index...")

for text in dummy_texts:
    vector = model.encode(text).tolist()
    insert_vector(vector, text)

print("Insertion complete!")