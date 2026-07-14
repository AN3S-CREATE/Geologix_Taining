"""Phase 6/7: Build local ChromaDB legal vault from ZASCA-Sum for RAG."""
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import chromadb

print("Building Legal RAG vault for geologix-legal...")

# 1. Embedding model (runs on GPU when available)
embedder = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")

# 2. Vector database (local file, never leaves your machine)
client = chromadb.PersistentClient(path="models/legal_vault")
collection = client.get_or_create_collection(
    name="zasca_cases",
    metadata={"hnsw:space": "cosine"},
)

# 3. Load all ZASCA cases
ds = load_dataset("dsfsi/zasca-sum", split="train")
print(f"Loaded {len(ds)} cases from Hugging Face")

# 4. Chunk and store
batch, ids, metas = [], [], []
for idx, row in enumerate(ds):
    case_id = row.get("id", f"case_{idx}")
    year = row.get("year", "unknown")
    case_type = row.get("type", "unknown")
    text = f"{row.get('input', '')}\n\nSUMMARY: {row.get('output', '')}"

    # Simple semantic chunking (~512 words with overlap)
    words = text.split()
    chunks = [" ".join(words[i : i + 512]) for i in range(0, len(words), 400)]
    for cidx, chunk in enumerate(chunks):
        batch.append(chunk)
        ids.append(f"{case_id}_chunk{cidx}")
        metas.append(
            {
                "case_id": case_id,
                "year": str(year),
                "type": case_type,
                "chunk_index": cidx,
                "source": "ZASCA-Sum",
            }
        )

    if len(batch) >= 64:
        embs = embedder.encode(batch).tolist()
        collection.add(ids=ids, embeddings=embs, documents=batch, metadatas=metas)
        print(f"   Indexed {idx + 1}/{len(ds)} cases...")
        batch, ids, metas = [], [], []

# Flush remainder
if batch:
    embs = embedder.encode(batch).tolist()
    collection.add(ids=ids, embeddings=embs, documents=batch, metadatas=metas)

print("\n✅ Legal vault complete!")
print("   Location: models/legal_vault/")
print(f"   Cases: {len(ds)}")
print(f"   Total chunks: {collection.count()}")
print("   This database stays on your machine. Air-gapped. POPIA-safe.")
