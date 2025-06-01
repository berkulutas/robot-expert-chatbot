from agents import kuka_db

question = "What is the repeatability of the Kuka KR 1000 1300?"
results = kuka_db.similarity_search(question, k=1)
for doc in results:
    print("\n=== CHUNK ===\n")
    print(doc.page_content)
