from agents import kuka_db

question = "which ar?"
results = kuka_db.similarity_search(question, k=1)
for doc in results:
    print("\n=== CHUNK ===\n")
    print(doc.page_content)
