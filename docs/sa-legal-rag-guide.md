
# 🔒 Company Legal AI: Fine-Tuned Brain + Secure Case Memory

## The Architecture (How It Works)

```
┌─────────────────────────────────────────────────────────────┐
│  Your Legal Team asks:                                      │
│  "What precedents support our argument in the Smith case?"  │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌─────────▼─────────┐
         │   RAG Retriever   │  Searches your case database
         │   (ChromaDB)      │  for relevant paragraphs
         └─────────┬─────────┘
                   │ "Found 3 similar cases + 2 evidence docs"
         ┌─────────▼─────────┐
         │  Fine-Tuned LLM   │  (Llama 3.1 8B on RTX 5070)
         │  + SA Legal Brain │  Reads the retrieved docs + reasons
         └─────────┬─────────┘
                   │ "Based on S v Makwanyane and the evidence
                   │  in Case 2024/45, the strongest argument is..."
         ┌─────────▼─────────┐
         │  Response with    │
         │  Source Citations │
         └───────────────────┘
```

**Why this is better than training on your cases:**
- **Privacy**: Case files are never baked into the model. They live in an encrypted local database.
- **Accuracy**: The model reads the *actual text* of your case, not a vague memory of it.
- **Flexibility**: Add a new case today, use it in the chatbot today. No retraining.
- **POPIA Compliance**: Personal information stays in your control, not in a cloud model.

---

## 🚨 Critical: Data Privacy & POPIA Checklist

Before you upload **any** company case file, you **must** sanitize it:

| Action | Why | Tool |
|--------|-----|------|
| **Remove client names** | POPIA protects personal identifiers | Manual search/replace |
| **Redact ID numbers** | Highly sensitive personal info | Python regex script |
| **Replace addresses** | Privacy risk | Replace with `[Address Redacted]` |
| **Remove banking details** | Financial POPIA data | Global find/replace |
| **Anonymize opposing parties** | Unless public record | Use `[Party A]` / `[Party B]` |
| **Keep legal strategy** | This is the valuable part! | ✅ Safe to keep |

**Golden Rule**: If you wouldn't email it to a stranger, don't put it in any system until sanitized.

---

## Phase 1: The "No-Code" Fast Track (Recommended for Beginners)

If your legal team wants to start using this **this week**, use a local RAG desktop app that connects to your Ollama model.

### Recommended Tool: AnythingLLM (or OpenWebUI)
These are free desktop applications that:
- Run **100% offline** on your RTX 5070
- Let you drag-and-drop PDFs/Word docs of your cases
- Automatically connect to your Ollama model
- Create a "South African Legal" workspace

**Setup:**
1. Install **Ollama** and your fine-tuned SA Legal model
2. Install **AnythingLLM** (or OpenWebUI)
3. Create a workspace called "Company Legal Cases"
4. Upload sanitized case files (PDFs, Word docs, emails)
5. Select your SA Legal model as the LLM
6. Start chatting: *"Summarize the evidence in Case 2024/45 and suggest weaknesses in the opposing argument."*

**Pros**: Zero coding. Legal team can use it immediately.  
**Cons**: Less customization for specific legal workflows.

---

## Phase 2: Custom Python RAG Pipeline (For Power Users)

If you want to build a tailored tool that integrates with your case management system, here's a complete starter script.

### Step 1: Prepare Your Case Documents

Create a folder structure:

```
company_cases/
├── case_2024_45_smith/
│   ├── pleadings.txt
│   ├── evidence_summary.txt
│   └── strategy_notes.txt
├── case_2023_12_jones/
│   ├── pleadings.txt
│   └── correspondence.txt
└── templates/
    └── successful_arguments.txt
```

**Format each file as:**
```text
CASE ID: 2024/45
PARTIES: [Company] v [Opponent]
STATUS: Discovery phase
COURT: Gauteng High Court, Pretoria

SECTION: Evidence
CONTENT: The witness testimony indicates that...

SECTION: Strategy
CONTENT: Our strongest argument rests on S v Makwanyane...
```

### Step 2: Install Local RAG Stack

```bash
pip install chromadb sentence-transformers ollama python-docx PyPDF2
```

### Step 3: Build the Knowledge Base

Save this as `build_case_memory.py`:

```python
import os
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
CASES_FOLDER = "./company_cases"
DB_PATH = "./legal_case_db"

# --- 1. LOCAL EMBEDDING MODEL ---
# This runs on your RTX 5070. It converts text into "searchable vectors"
print("Loading embedding model...")
embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")

# --- 2. CREATE LOCAL DATABASE ---
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(
    name="company_cases",
    metadata={"hnsw:space": "cosine"}
)

# --- 3. LOAD AND CHUNK CASE FILES ---
def chunk_text(text, chunk_size=512, overlap=100):
    """Split long documents into overlapping chunks for better retrieval."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

print("Processing case files...")
case_files = []

for root, dirs, files in os.walk(CASES_FOLDER):
    for file in files:
        if file.endswith((".txt", ".md")):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create semantic chunks
            chunks = chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                case_files.append({
                    "id": f"{file}_{i}",
                    "text": chunk,
                    "metadata": {
                        "source": file,
                        "folder": os.path.basename(root),
                        "chunk_index": i
                    }
                })

# --- 4. GENERATE EMBEDDINGS AND STORE ---
print(f"Embedding {len(case_files)} chunks...")

for i in range(0, len(case_files), 32):  # Batch size 32
    batch = case_files[i:i+32]
    texts = [item["text"] for item in batch]
    ids = [item["id"] for item in batch]
    metadatas = [item["metadata"] for item in batch]
    
    # Generate embeddings on GPU
    embeddings = embed_model.encode(texts, convert_to_numpy=True).tolist()
    
    # Store in ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

print("Knowledge base created! Ready for queries.")
```

### Step 4: Query with Your Legal Brain

Save this as `query_legal_assistant.py`:

```python
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
DB_PATH = "./legal_case_db"
OLLAMA_MODEL = "sa-legal-lora"  # Your fine-tuned model from earlier

# --- 1. LOAD COMPONENTS ---
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_collection("company_cases")

embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")

# --- 2. QUERY FUNCTION ---
def ask_legal_assistant(question, n_results=5):
    # Convert question to vector
    query_embedding = embed_model.encode([question], convert_to_numpy=True).tolist()
    
    # Find relevant case chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    # Build context from retrieved case files
    context = ""
    sources = []
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        context += f"\n--- DOCUMENT {i+1} [Source: {meta['folder']}/{meta['source']}] ---\n{doc}\n"
        sources.append(f"{meta['folder']}/{meta['source']}")
    
    # Build the prompt for your fine-tuned legal model
    system_prompt = """You are a senior South African legal research assistant. 
You have access to the company's case files and general South African legal knowledge.
Base your answer strictly on the provided case documents and legal principles.
Always cite the specific case or document you are referencing.
If you cannot find support in the documents, say so clearly.
Remember: You are not a substitute for professional legal advice."""

    full_prompt = f"""{system_prompt}

COMPANY CASE DOCUMENTS:
{context}

LEGAL QUESTION: {question}

Provide a structured legal analysis with:
1. Relevant precedents or case documents
2. Suggested legal arguments
3. Potential risks or weaknesses
4. Recommended next steps"""

    # Query your local Ollama model
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        options={"temperature": 0.3}  # Lower = more factual for legal work
    )
    
    return {
        "answer": response["message"]["content"],
        "sources": list(set(sources))  # Remove duplicates
    }

# --- 3. INTERACTIVE LOOP ---
if __name__ == "__main__":
    print("🏛️ South African Legal Case Assistant")
    print("Type 'exit' to quit\n")
    
    while True:
        question = input("Ask: ")
        if question.lower() == "exit":
            break
            
        print("\n🔍 Searching case database...")
        result = ask_legal_assistant(question)
        
        print("\n" + "="*60)
        print("RESPONSE:")
        print(result["answer"])
        print("\n" + "-"*60)
        print("REFERENCED CASES/DOCUMENTS:")
        for src in result["sources"]:
            print(f"  • {src}")
        print("="*60 + "\n")
```

### How to Use

```bash
# 1. Build your knowledge base (run once per case batch)
python build_case_memory.py

# 2. Start querying
python query_legal_assistant.py

# Example questions:
# > "What evidence do we have in Case 2024/45 regarding breach of contract?"
# > "Which precedents support our argument for specific performance?"
# > "Summarize the opposing counsel's strategy in the Jones matter."
# > "What are the weaknesses in our discovery for Case 2023/12?"
```

---

## Phase 3: Advanced — Fine-Tuning on Sanitized Case Patterns

Once you have 50+ closed cases with **known outcomes**, you can create a second, smaller training dataset of **anonymized case summaries** to teach the model *strategic patterns*:

**Example training entry:**
```json
{
  "instruction": "Analyze the following case facts and recommend the strongest legal strategy for a South African High Court contract dispute.",
  "input": "Facts: [Company A] entered a service agreement with [Company B]. Payment was withheld due to alleged non-performance. Key evidence includes email correspondence and witness testimony. Precedent cases in our firm: [Case 2021/03], [Case 2022/17].",
  "output": "Recommended strategy: 1) File for specific performance rather than damages, based on the precedent in [Case 2021/03] where the court favored... 2) Lead with the email evidence as it directly contradicts the opposing party's defense... 3) Risk: The witness is a former employee, which may affect credibility under cross-examination per S v Phoolan..."
}
```

**This is NOT the full case file** — it's a strategic summary. The full files stay in the RAG database.

---

## 🛡️ Security Best Practices for Your Legal Team

| Rule | Implementation |
|------|----------------|
| **Air-gapped setup** | Run the RTX 5070 machine offline. No internet. |
| **No cloud upload** | Never use Google Colab for company case files. |
| **Access control** | Use OS-level user accounts on the RAG machine. |
| **Encrypted storage** | Store case files and vector DB on an encrypted drive. |
| **Audit logging** | Log all queries to know who asked what. |
| **Regular purging** | Delete closed case data from RAG when retention period ends. |

---

## Recommended Workflow for Your Team

**Week 1**: Set up Ollama + AnythingLLM on the RTX 5070. Upload 5 sanitized closed cases. Test queries.  
**Week 2**: Train the SA Legal fine-tuned model (from the previous guide). Swap it into AnythingLLM.  
**Week 3**: Add current open cases to the RAG database. Train legal staff on prompt writing.  
**Week 4**: Build the Python pipeline for custom integrations (e.g., linking to your existing practice management software).

---

## Example Prompts for Successful Outcomes

| Goal | Prompt |
|------|--------|
| **Case strategy** | "Based on the facts in [Case X] and retrieved precedents, what are the three strongest arguments for summary judgment, and what are the risks of each?" |
| **Discovery prep** | "Review the pleadings in [Case Y] and identify all document categories we should request in discovery." |
| **Opposition analysis** | "Analyze the opposing counsel's argument in [Case Z]. What precedents undermine their position, and what evidence should we gather to counter it?" |
| **Settlement advice** | "Given the strengths and weaknesses visible in [Case A], what is a reasonable settlement range, and what negotiating points should we emphasize?" |
| **Drafting aid** | "Draft a notice of motion for specific performance based on the facts and precedent cases retrieved for [Case B]." |

---

## Summary

- **Fine-tune on ZASCA-Sum** → Gives your model a South African legal brain.
- **Use RAG for company cases** → Keeps confidential data secure and retrievable.
- **Sanitize all case files** → Remove PII to comply with POPIA before adding to any system.
- **Run everything locally** → Your RTX 5070 is perfect for this. No cloud needed.

**Start with AnythingLLM + Ollama this week.** It will give your legal team immediate value while you build the custom Python pipeline in the background.
