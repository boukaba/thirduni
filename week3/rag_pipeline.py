"""RAG essentials: two pipelines + the silent embedding-mismatch failure.

Ingestion (once):    docs -> chunks -> embedding model A -> vector store
Retrieval (per ask): question -> embedding model -> nearest vectors -> chunks -> prompt

The failure: same store, query embedded with a different model of the SAME
dimension (both 3072 here). No errors, no warnings. Wrong chunks, ranked fine.
"""

from dotenv import load_dotenv

load_dotenv()

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI

# ingestion-side embedding model
model_a = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
# query-side model, different space, same size (the bug)
model_b = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

CHUNKS = [
    "SpaceX launched Starship on its fifth test flight from Boca Chica in October 2024. The booster returned to the launch tower and was caught by the chopstick arms.",
    "Microsoft announced a new version of SQL Server with built-in vector search and tighter Azure integration, aimed at enterprise data teams.",
    "Payment failures in e-commerce are often caused by expired cards, insufficient funds, or 3D Secure timeouts. Retry logic with backoff recovers a surprising number of them.",
    "The employee handbook grants 20 days of paid vacation in the first year, rising to 25 after three years of service.",
    "The pharmacy leaflet explains that the medicine should be stored below 25C and taken once daily with food.",
    "Tender compliance in Algeria requires a tax certificate, commercial registry extract, and technical datasheets for every listed machine.",
]

store = InMemoryVectorStore(model_a)
store.add_texts(CHUNKS)

question = "What did SpaceX launch and when?"

if __name__ == "__main__":
    print("=== healthy: query embedded with model A ===")
    for doc, score in store.similarity_search_with_score(question, k=3):
        print(f"score={score:.4f} | {doc.page_content[:72]}")

    print()
    print("=== mismatch: same query embedded with model B (same 3072 dims) ===")
    q_vec_b = model_b.embed_query(question)
    top = store.similarity_search_with_score_by_vector(q_vec_b, k=3)
    for doc, score in top:
        print(f"score={score:.4f} | {doc.page_content[:72]}")

    print()
    print("=== what the model does with the wrong chunks ===")
    llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY"))
    prompt = "Answer using only these retrieved documents:\n\n" + "\n\n".join(d.page_content for d, _ in top) + f"\n\nQuestion: {question}"
    print(str(llm.invoke(prompt).content)[:300])
