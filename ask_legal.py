"""Interactive legal Q&A: ZASCA RAG vault + geologix-legal via Ollama."""
from sentence_transformers import SentenceTransformer
import chromadb
import ollama

print("=" * 60)
print("⚖️ GEOLIX LEGAL — SA Case Law + Ollama Query Interface")
print("   Model: geologix-legal")
print("   Vault: ZASCA-Sum (4,000+ SCA judgments)")
print("=" * 60)

# Load vault
embedder = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")
client = chromadb.PersistentClient(path="models/legal_vault")
collection = client.get_collection("zasca_cases")


def ask(question):
    # 1. Find relevant cases
    q_embed = embedder.encode([question]).tolist()
    results = collection.query(
        query_embeddings=q_embed,
        n_results=5,
        include=["documents", "metadatas"],
    )

    # 2. Build context
    context = ""
    sources = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context += f"\n[Case {meta['case_id']} ({meta['year']})]\n{doc[:800]}...\n"
        sources.append(f"{meta['case_id']} ({meta['year']})")

    # 3. Send to geologix-legal via Ollama with retrieved context
    prompt = f"""SA LEGAL CASES RETRIEVED FROM VAULT:
{context}

LEGAL QUESTION: {question}

Answer using the retrieved cases and your training knowledge. Cite specific case names and legal principles. Structure as IRAC."""
    response = ollama.chat(
        model="geologix-legal",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2, "num_ctx": 4096},
    )

    return response["message"]["content"], sources


# Interactive loop
while True:
    q = input("\nLegal Question > ").strip()
    if q.lower() in ["exit", "quit"]:
        break
    if not q:
        continue

    print("🔍 Searching ZASCA vault...")
    answer, sources = ask(q)

    print("\n┌── GEOLIX LEGAL RESPONSE ──")
    print("│")
    print(f"│ {answer}")
    print("│")
    print(f"│ Sources: {', '.join(sources)}")
    print("└─────────────────────────────")
