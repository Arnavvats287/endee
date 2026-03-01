from agent.rag_tool import rag_search

query = "How will employees be notified about major policy changes?"

print(f"Querying RAG pipeline:\n{query}\n")

response = rag_search(query)

print("RAG-generated response:\n")
print(response)